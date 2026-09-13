from notion_client import Client
import os
from datetime import datetime

notion = Client(auth=os.environ["NOTION_TOKEN"])

MAX_TABLE_ROWS = 20


def _chunk_text(text: str, max_length: int = 2000) -> list[str]:
    """Split text into chunks under Notion's 2000-char block limit."""
    if len(text) <= max_length:
        return [text]
    chunks = []
    paragraphs = text.split("\n\n")
    current = ""
    for para in paragraphs:
        if len(current) + len(para) + 2 <= max_length:
            current = f"{current}\n\n{para}" if current else para
        else:
            if current:
                chunks.append(current)
            while len(para) > max_length:
                chunks.append(para[:max_length])
                para = para[max_length:]
            current = para
    if current:
        chunks.append(current)
    return chunks


def _build_video_table(videos: list[dict]) -> dict:
    """Build a native Notion table block from the scraped video list."""
    headers = ["Views", "Caption", "Author", "Sound", "URL", "Likes", "Comments"]
    rows = videos[:MAX_TABLE_ROWS]

    def cell(text: str) -> list[dict]:
        return [{"type": "text", "text": {"content": str(text)[:190]}}]

    header_row = {
        "object": "block",
        "type": "table_row",
        "table_row": {"cells": [cell(h) for h in headers]},
    }

    data_rows = []
    for v in rows:
        data_rows.append({
            "object": "block",
            "type": "table_row",
            "table_row": {
                "cells": [
                    cell(f"{v.get('views', 0):,}"),
                    cell(v.get("caption", "")),
                    cell(v.get("author", "")),
                    cell(v.get("sound", "")),
                    cell(v.get("url", "")),
                    cell(f"{v.get('likes', 0):,}"),
                    cell(f"{v.get('comments', 0):,}"),
                ]
            },
        })

    return {
        "object": "block",
        "type": "table",
        "table": {
            "table_width": len(headers),
            "has_column_header": True,
            "has_row_header": False,
            "children": [header_row] + data_rows,
        },
    }


def create_trend_report(niche: str, executive_summary: str, videos: list[dict]) -> str:
    """Create a Notion page with an executive summary and a table of scraped videos."""
    today_us = datetime.now().strftime("%m/%d/%Y")
    title = f"Tiktok trends {today_us}: {niche} hashtag"

    summary_blocks = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"text": {"content": chunk}}]},
        }
        for chunk in _chunk_text(executive_summary)
    ]

    table_block = _build_video_table(videos)

    children = (
        [{"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "Executive Summary"}}]}}]
        + summary_blocks
        + [{"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "Scraped Videos"}}]}}]
        + [table_block]
    )

    page = notion.pages.create(
        parent={"page_id": os.environ["NOTION_PARENT_PAGE_ID"]},
        properties={"title": [{"text": {"content": title}}]},
        children=children,
    )
    return page["url"]