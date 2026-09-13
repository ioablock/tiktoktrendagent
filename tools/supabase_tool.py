from supabase import create_client
import os

sb = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

def log_run(niche: str, videos: list[dict], notion_url: str, status: str, used_fallback: bool = False) -> str:
    """Log a completed agent run, including the full video data, for auditing."""
    sb.table("runs").insert({
        "niche": niche,
        "video_count": len(videos),
        "viral_count": len(videos),
        "used_fallback": used_fallback,
        "notion_url": notion_url,
        "status": status,
        "videos": videos,
    }).execute()
    return "logged"