# scraper.py
import feedparser
import json
import os
from datetime import datetime

SOURCES_RSS = {
    "Hespress":  "https://www.hespress.com/feed",
    "Médias24":  "https://www.medias24.com/feed",
    "Le360":     "https://www.le360.ma/rss.xml",
}

def scrape_rss():
    articles = []
    for source, url in SOURCES_RSS.items():
        try:
            feed = feedparser.parse(url)
            print(f"[{source}] {len(feed.entries)} articles trouvés")
            
            for entry in feed.entries[:10]:  # 10 derniers par source
                articles.append({
                    "source":      source,
                    "titre":       entry.get("title", ""),
                    "description": entry.get("summary", "")[:300],
                    "url":         entry.get("link", ""),
                    "date":        entry.get("published", ""),
                    "categorie":   "macro",   # à affiner plus tard
                })
        except Exception as e:
            print(f"[{source}] Erreur : {e}")
    return articles


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    
    articles = scrape_rss()
    
    # Trier par date décroissante
    articles.sort(key=lambda a: a.get("date", ""), reverse=True)
    
    data = {
        "last_update": datetime.now().isoformat(),
        "articles": articles,
    }
    
    with open("data/actualites.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ {len(articles)} articles écrits dans data/actualites.json")