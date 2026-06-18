from datetime import datetime, timedelta
from fastapi import APIRouter, BackgroundTasks

from app.database import get_connection
from app.scraper import scrape_rss, cache
from app.config import CACHE_TTL


# APIRouter = a "mini FastAPI app" you can plug into the main app
router = APIRouter()


@router.get("/news")
async def get_news(background_tasks: BackgroundTasks):
    now = datetime.utcnow()

    # Always kick off a fresh scrape in the background
    background_tasks.add_task(scrape_rss)

    # CACHE HIT
    if cache["data"] is not None and cache["expires_at"] > now:
        return {
            "source": "cache",
            "count": len(cache["data"]),
            "articles": cache["data"],
        }

    # CACHE MISS -> read from DB
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, title, link, summary, saved_at FROM articles ORDER BY id DESC LIMIT 20"
    )
    rows = cursor.fetchall()
    conn.close()

    articles = [
        {"id": r[0], "title": r[1], "link": r[2], "summary": r[3], "saved_at": r[4]}
        for r in rows
    ]

    cache["data"] = articles
    cache["expires_at"] = now + timedelta(seconds=CACHE_TTL)

    return {
        "source": "database",
        "count": len(articles),
        "articles": articles,
    }