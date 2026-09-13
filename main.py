# main.py
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request, BackgroundTasks
import httpx
from agent import agent

app = FastAPI()

@app.post("/slack/trendcheck")
async def trendcheck(request: Request, background_tasks: BackgroundTasks):
    form = await request.form()
    raw_text = form.get("text", "").strip()
    response_url = form.get("response_url")

    if not raw_text:
        return {
            "response_type": "ephemeral",
            "text": "Please provide a hashtag, e.g. `/trendcheck tech`",
        }

    niche = raw_text.lstrip("#").lower()

    print(f"[trendcheck] Received request for niche: {niche}")

    background_tasks.add_task(run_agent_and_reply, niche, response_url)

    return {"response_type": "ephemeral", "text": f"🔍 Scraping TikTok trends for *{niche}*..."}

async def run_agent_and_reply(text: str, response_url: str):
    print(f"[run_agent_and_reply] Starting agent for niche: {text}")
    try:
        result = agent.invoke({"messages": [{"role": "user", "content": f"niche={text}"}]})
        final_message = result["messages"][-1].content
        print(f"[run_agent_and_reply] SUCCESS: {final_message}")
        payload = {"response_type": "in_channel", "text": f"✅ Done! {final_message}"}
    except Exception as e:
        print(f"[run_agent_and_reply] FAILED: {e}")
        import traceback
        traceback.print_exc()
        payload = {"response_type": "ephemeral", "text": f"❌ Something went wrong: {e}"}
    async with httpx.AsyncClient() as client:
        await client.post(response_url, json=payload)
    print("[run_agent_and_reply] Posted result to response_url")