from dotenv import load_dotenv
load_dotenv()

from notion_tool import create_trend_report

url = create_trend_report(
    niche="tech",
    synthesis_markdown="This is a test synthesis paragraph to confirm the Notion integration works end to end."
)
print(f"Page created: {url}")