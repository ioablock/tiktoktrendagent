from dotenv import load_dotenv
load_dotenv()

from apify_tool import scrape_tiktok_trends

results = scrape_tiktok_trends("tech")
print(f"Got {len(results)} viral videos\n")

for r in results:
    print(f"Caption:  {r['caption']}")
    print(f"Author:   {r['author']}")
    print(f"Sound:    {r['sound']}")
    print(f"Views:    {r['views']:,}")
    print(f"Likes:    {r['likes']:,}")
    print(f"Comments: {r['comments']:,}")
    print(f"Shares:   {r['shares']:,}")
    print(f"Posted:   {r['post_date']}")
    print(f"URL:      {r['url']}")
    print("-" * 60)