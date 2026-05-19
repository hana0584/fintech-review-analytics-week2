import time
import pandas as pd
from google_play_scraper import Sort, reviews
from datetime import datetime
from tqdm import tqdm

def scrape_app_reviews(app_id, app_name, count=500):
    """
    Scrape reviews from Google Play Store for a given app
    
    Args:
        app_id: Google Play package name (e.g., 'com.cbe.mobile')
        app_name: Display name for the app
        count: Number of reviews to scrape (default 500)
    
    Returns:
        List of dictionaries containing review data
    """
    all_reviews = []
    
    print(f"\n📱 Scraping {app_name} ({app_id})")
    print(f"Target: {count} reviews")
    
    try:
        
        result, token = reviews(
            app_id,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=min(count, 200)
        )
        all_reviews.extend(result)
        
        
        while len(all_reviews) < count and token:
            result, token = reviews(
                app_id,
                continuation_token=token
            )
            all_reviews.extend(result)
            time.sleep(2)  
            print(f"  Progress: {len(all_reviews)}/{count} reviews...")
        
    except Exception as e:
        print(f"   Error scraping {app_name}: {e}")
        return []
    
    
    formatted_reviews = []
    for review in all_reviews[:count]:
        formatted_reviews.append({
            'review': review.get('content', ''),
            'rating': review.get('score', 0),
            'date': review.get('at'),
            'bank': app_name,
            'source': 'Google Play'
        })
    
    print(f"   Collected {len(formatted_reviews)} reviews")
    return formatted_reviews

def scrape_all_banks():
    """
    Scrape reviews for all three Ethiopian banks
    """
   
    bank_apps = {
     'Commercial Bank of Ethiopia': 'com.combanketh.mobilebanking',
      'Bank of Abyssinia': 'com.boa.boaMobileBanking',
    'Dashen Bank': 'com.dashen.dashensuperapp' 
    }
    
    all_reviews = []
    
    for bank_name, app_id in bank_apps.items():
        reviews_data = scrape_app_reviews(app_id, bank_name, count=400)
        all_reviews.extend(reviews_data)
        time.sleep(3) 
    
    return all_reviews

if __name__ == "__main__":
    reviews_data = scrape_all_banks()
    print(f"\n Total reviews collected: {len(reviews_data)}")
    
    
    import os
    os.makedirs('data/raw', exist_ok=True)
    
    df = pd.DataFrame(reviews_data)
    df.to_csv('data/raw/raw_reviews.csv', index=False)
    print(" Raw data saved to data/raw/raw_reviews.csv")