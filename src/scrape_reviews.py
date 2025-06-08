# File: src/scrape_reviews.py

from google_play_scraper import reviews
import pandas as pd
import os

apps = {
    "CBE": "com.combanketh.mobilebanking",
    "Dashen": "com.dashen.dashensuperapp",
    "BOA": "com.boa.boaMobileBanking"
}

all_reviews = []

for bank, package in apps.items():
    print(f"🛠️ Scraping reviews for {bank}...")
    result, _ = reviews(
        package,
        lang='en',
        country='et',
        count=500  
    )

    for r in result:
        all_reviews.append({
            "review": r.get("content", ""),
            "rating": r.get("score", None),
            "date": r.get("at").strftime("%Y-%m-%d") if r.get("at") else None,
            "bank": bank,
            "source": "Google Play"
        })

df = pd.DataFrame(all_reviews)

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Preprocessing
if not df.empty:
    print("➡️ Columns:", df.columns.tolist())
    df.drop_duplicates(subset=["review"], inplace=True)
    df.dropna(subset=["review", "rating", "date"], inplace=True)
    df.to_csv("data/bank_reviews.csv", index=False)
    print("✅ Done. Data saved to data/bank_reviews.csv")
else:
    print("⚠️ No reviews scraped! Check package IDs or network.")

