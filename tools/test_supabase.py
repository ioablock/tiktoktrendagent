from dotenv import load_dotenv
load_dotenv()

import os
print("Loaded URL:", os.environ.get("SUPABASE_URL"))
print("Loaded KEY:", os.environ.get("SUPABASE_KEY"))

from supabase_tool import log_run

fake_videos = [
    {
        "caption": "This is AI (artificial intelligence)",
        "author": "laurenisacommonname",
        "sound": "Welp, Didn't Expect That",
        "likes": 233,
        "views": 26100,
        "comments": 32,
        "shares": 49,
        "post_date": "2026-07-22T23:00:04.000Z",
        "url": "https://www.tiktok.com/@laurenisacommonname/video/7665490933453983007",
    }
]

result = log_run(
    niche="tech",
    videos=fake_videos,
    notion_url="https://www.notion.so/fake-test-page",
    status="success",
    used_fallback=False,
)
print(result)