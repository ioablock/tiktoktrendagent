<div align="center">

# 📈 TrendPilot

### AI agent that turns viral TikTok trends into ready-to-use marketing insights — straight from Slack

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![DeepAgents](https://img.shields.io/badge/DeepAgents-Agent%20Harness-6E56CF)](https://github.com/langchain-ai/deepagents)
[![Slack](https://img.shields.io/badge/Slack-Trigger-4A154B?logo=slack&logoColor=white)](https://slack.com)
[![Apify](https://img.shields.io/badge/Apify-Scraping-00C0B5?logo=apify&logoColor=white)](https://apify.com)
[![Notion](https://img.shields.io/badge/Notion-Deliverable-000000?logo=notion&logoColor=white)](https://notion.so)
[![Supabase](https://img.shields.io/badge/Supabase-Verification-3ECF8E?logo=supabase&logoColor=white)](https://supabase.com)

</div>

---
## Video Presentation link
https://canva.link/u3m6qbbpqx5cx85

## 🧠 What it does

**TrendPilot** is a multistep AI agent built for marketers who need to know what's trending on TikTok in their niche — without spending twenty minutes scrolling for it.

A marketer types one Slack command with a hashtag. The agent scrapes the top trending videos for that hashtag, analyzes them for recurring patterns and content angles, and delivers a clean executive brief to Notion — complete with a full data table of every video it found. Every run is logged for auditability, so there's always a record of what the agent found and when.

<table>
<tr><td width="120"><b>🎯 Trigger</b></td><td>Slack slash command</td></tr>
<tr><td><b>🕷️ Data</b></td><td>Apify (TikTok Hashtag Scraper)</td></tr>
<tr><td><b>📄 Deliverable</b></td><td>Notion (executive brief + video table)</td></tr>
<tr><td><b>🗂️ Verification</b></td><td>Supabase (run log)</td></tr>
</table>

### External apps this agent connects to

| # | App | Role |
|---|-----|------|
| 1 | **Slack** | Entry point — the marketer triggers a run and receives the result |
| 2 | **Apify** | Scrapes TikTok for trending videos under a given hashtag |
| 3 | **Notion** | Hosts the generated executive brief and video data table |
| 4 | **Supabase** | Logs every run for auditability and verification |

---

## ⚙️ How it works

<div align="center">

```
   👤 Marketer                🤖 Agent Pipeline                    📬 Output
┌────────────────┐      ┌──────────────────────────┐      ┌─────────────────────┐
│  Slack          │      │                          │      │                     │
│  /trendcheck ai │ ───▶ │  1. Scrape TikTok (Apify)│      │                     │
│                 │      │  2. Synthesize trends    │      │  📄 Notion page      │
│                 │      │  3. Write Notion report  │ ───▶ │  🗂️ Supabase log     │
│                 │      │  4. Log run (Supabase)   │      │  💬 Slack reply      │
│                 │ ◀─────────────────────────────────────  with link            │
└────────────────┘      └──────────────────────────┘      └─────────────────────┘
```

</div>

<br>

<table>
<tr>
<td width="40" align="center">1️⃣</td>
<td><b>The marketer types a command in Slack</b><br>
<code>/trendcheck ai</code> — no dashboard, no login, just a hashtag typed into a channel they already live in. Slack instantly replies with a "🔍 Scraping..." acknowledgment so they know it's working.</td>
</tr>
<tr>
<td align="center">2️⃣</td>
<td><b>The agent scrapes TikTok via Apify</b><br>
Using the <code>clockworks/tiktok-hashtag-scraper</code> Actor, it pulls the most-viewed recent videos under that hashtag — caption, author, sound, views, likes, comments, shares, and URL for each. If the hashtag doesn't return enough high-performing videos, the agent automatically relaxes its view threshold rather than guessing at unverified hashtag variants, so it always returns a usable result.</td>
</tr>
<tr>
<td align="center">3️⃣</td>
<td><b>The agent reasons over the data</b><br>
Instead of listing videos one by one, it identifies the underlying patterns — recurring formats, hooks, and angles — and writes a concise executive summary explaining <i>why</i> each pattern is working and whether it's rising or already peaking.</td>
</tr>
<tr>
<td align="center">4️⃣</td>
<td><b>A report is created in Notion</b><br>
Titled <code>Tiktok trends &lt;date&gt;: &lt;hashtag&gt; hashtag</code>, the page contains the executive summary followed by a full data table of every scraped video (views, caption, author, sound, URL, likes, comments) — a marketer can skim the summary or dig into the raw data.</td>
</tr>
<tr>
<td align="center">5️⃣</td>
<td><b>The run is logged to Supabase</b><br>
Niche, video count, view threshold used, the Notion link, and a success/failure status are recorded — a running, queryable audit trail proving the agent works reliably across different hashtags and runs, not just in a single demo.</td>
</tr>
<tr>
<td align="center">6️⃣</td>
<td><b>Slack gets the final word</b><br>
Once everything completes, the agent posts back in the same Slack channel: <b>"✅ Done!"</b> with a direct link to the finished Notion report — the marketer never has to leave Slack to know it's ready.</td>
</tr>
</table>

---

## 🧩 Tech stack

- **Agent harness:** [DeepAgents](https://github.com/langchain-ai/deepagents) (built on LangGraph)
- **Backend:** FastAPI + Uvicorn
- **LLM:** Google Gemini (via `langchain-google-genai`)
- **Scraping:** Apify (`clockworks/tiktok-hashtag-scraper`)
- **Delivery:** Notion API
- **Logging:** Supabase (Postgres)
- **Trigger:** Slack slash commands

---

## 🚀 Setup

```bash
git clone https://github.com/YOUR_USERNAME/TrendPilot.git
cd TrendPilot
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your own credentials:

```
APIFY_TOKEN=
NOTION_TOKEN=
NOTION_PARENT_PAGE_ID=
SUPABASE_URL=
SUPABASE_KEY=
GOOGLE_API_KEY=
```

Run the server:

```bash
uvicorn main:app --reload
```

Expose it publicly with [ngrok](https://ngrok.com) and point your Slack app's `/trendcheck` slash command Request URL to:

```
https://YOUR_NGROK_URL/slack/trendcheck
```

---

<div align="center">

Built in one day for a hackathon 🛠️

</div>
