
from google_play_scraper import search

banks = [
    "Commercial Bank of Ethiopia",
    "Bank of Abyssinia", 
    "Dashen Bank Ethiopia"
]

for bank in banks:
    print(f"\nSearching for: {bank}")
    results = search(bank, lang='en', country='us', n_hits=5)
    for r in results:
        print(f"  {r['title']}: {r['appId']}")