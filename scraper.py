from datetime import datetime
import httpx      #difference between httpx and http
import feedparser

from database import get_connection
from similarity import jaccard
from config import FEEDS, DUPLICATION_THRESHOLD, ALERT_WORDS

cache = [
    "data" : NONE,
    "expiresat" : datetime.min,
]

async def scraperss():
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT title FROM articles ORDER BY id DESC LIMIT 50")
    recent_titles = [row[0] for row in cursor.fetchall()]

    async with httpx.AsyncClient() as http:
        for feed_url in FEEDS:
            
            try:
                response = await http.get(feed_url, timeout=10.0)
                feed = feedparser.parse(response.text)

                for entry in feed.entries:
                    title = entry.get("title", "")
                    link = entry.get("link", "")
                    summary = entry.get("summary", "")

                    if not title or not link:
                        continue

                    # GATE 1: URL already exists?
                    cursor.execute("SELECT 1 FROM articles WHERE link = ?", (link,))
                    if cursor.fetchone():
                        continue

                    # GATE 2: Headline too similar to a recent one?
                    is_duplicate = any(
                        jaccard(title, old) >= DUPLICATION_THRESHOLD
                        for old in recent_titles
                    )
                    if is_duplicate:
                        continue

                    # SAVE
                    cursor.execute(
                        "INSERT INTO articles (title, link, summary, saved_at) VALUES (?, ?, ?, ?)",
                        (title, link, summary, datetime.utcnow().isoformat())
                    )
                    conn.commit()
                    recent_titles.append(title)

                    # GATE 3: Alert keyword match?
                    if any(word in title.lower() for word in ALERT_WORDS):
                        print(f"[ALERT] {title}")
                        
                        
            except Exception as error:
                print(f"[SCRAPE ERROR] {feed_url}: {error}")

    conn.close()
    cache["data"] = None 
                        
