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
    """Scrape TikTok videos for a given niche hashtag, in a single API call.
    Filters to videos meeting MIN_VIEWS; if fewer than MIN_VIRAL_COUNT qualify,
    progressively relaxes the threshold on the SAME scraped data (no extra
    scrapes) to conserve Apify usage.
    Returns a dict with 'videos', 'used_fallback', and 'effective_min_views'.
    """
    all_videos = _run_scrape([niche], results_per_page=50)  # one call only
    viral = [v for v in all_videos if v["views"] >= MIN_VIEWS]
    used_fallback = False
    effective_min_views = MIN_VIEWS

    if len(viral) < MIN_VIRAL_COUNT:
        used_fallback = True
        for t in [5_000, 2_000, 1_000, 0]:
            effective_min_views = t
            viral = [v for v in all_videos if v["views"] >= t]
            if len(viral) >= MIN_VIRAL_COUNT:
                break

    viral.sort(key=lambda v: v["views"], reverse=True)
    return {
        "videos": viral,
        "used_fallback": used_fallback,
        "effective_min_views": effective_min_views,
    }