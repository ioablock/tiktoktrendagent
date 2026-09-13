from apify_client import ApifyClient
import os

client = ApifyClient(os.environ["APIFY_TOKEN"])

MIN_VIEWS = 10_000
MIN_VIRAL_COUNT = 5

def _run_scrape(hashtags: list[str], results_per_page: int) -> list[dict]:
    run = client.actor("clockworks/tiktok-hashtag-scraper").call(run_input={
        "hashtags": hashtags,
        "resultsPerPage": results_per_page,
        "shouldDownloadCovers": False,
        "shouldDownloadSlideshowImages": False,
        "shouldDownloadSubtitles": False,
        "shouldDownloadVideos": False,
    })
    items = client.dataset(run.default_dataset_id).list_items().items
    return [
        {
            "caption": i.get("text"),
            "author": i.get("authorMeta", {}).get("name"),
            "sound": i.get("musicMeta", {}).get("musicName"),
            "likes": i.get("diggCount"),
            "views": i.get("playCount"),
            "comments": i.get("commentCount"),
            "shares": i.get("shareCount"),
            "post_date": i.get("createTimeISO"),
            "url": i.get("webVideoUrl"),
        }
        for i in items
        if "errorCode" not in i and i.get("playCount") is not None
    ]

def scrape_tiktok_trends(niche: str) -> dict:
    """Scrape viral TikTok videos (>=10K views) for a given niche.
    Widens the hashtag search if fewer than 5 viral videos are found.
    Returns a dict with 'videos' (list) and 'used_fallback' (bool).
    """
    all_videos = _run_scrape([niche], results_per_page=100)
    viral = [v for v in all_videos if v["views"] >= MIN_VIEWS]
    used_fallback = False

    if len(viral) < MIN_VIRAL_COUNT:
        used_fallback = True
        related_tags = [f"{niche}tok", f"{niche}tips"]  # dropped duplicate niche
        more_videos = _run_scrape(related_tags, results_per_page=150)
        combined = {v["url"]: v for v in (all_videos + more_videos)}.values()
        viral = [v for v in combined if v["views"] >= MIN_VIEWS]

    viral.sort(key=lambda v: v["views"], reverse=True)
    return {"videos": viral, "used_fallback": used_fallback}