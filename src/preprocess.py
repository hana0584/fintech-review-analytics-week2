import pandas as pd
import re
from datetime import datetime

def clean_text(text):
    """
    Clean review text by removing special characters and extra spaces
    """
    if pd.isna(text):
        return ""
    
    text = str(text)
   
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text) 
    
    text = ' '.join(text.split())
    return text

def normalize_date(date_str):
    """
    Convert various date formats to YYYY-MM-DD
    """
    if pd.isna(date_str):
        return None
    
    try:
       
        if isinstance(date_str, datetime):
            return date_str.strftime('%Y-%m-%d')
        elif isinstance(date_str, str):
          
            for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%b %d, %Y', '%B %d, %Y']:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.strftime('%Y-%m-%d')
                except ValueError:
                    continue
        return None
    except Exception:
        return None

def preprocess_reviews(df):
    """
    Full preprocessing pipeline
    """
    print("🔧 Starting preprocessing...")
    initial_count = len(df)
    
   
    duplicates = df.duplicated(subset=['review', 'bank']).sum()
    df = df.drop_duplicates(subset=['review', 'bank'])
    print(f"  Removed {duplicates} duplicate reviews")
    
   
    missing_review = df['review'].isna().sum()
    missing_rating = df['rating'].isna().sum()
    
   
    df = df.dropna(subset=['review', 'rating'])
    print(f"  Dropped {missing_review} rows with missing review text")
    print(f"  Dropped {missing_rating} rows with missing rating")
    
   
    df['review'] = df['review'].apply(clean_text)
    df = df[df['review'].str.len() > 0]
    df['date'] = df['date'].apply(normalize_date)
    df['rating'] = df['rating'].astype(int)
    df['review_length'] = df['review'].str.len()
    
    final_count = len(df)
    print(f"  Final dataset: {final_count} reviews (kept {final_count/initial_count*100:.1f}%)")
    
    return df

def save_cleaned_data(df, output_path='data/cleaned_reviews.csv'):
    """
    Save cleaned dataset to CSV
    """
    import os
    os.makedirs('data', exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f" Cleaned data saved to {output_path}")
    return df

def generate_data_quality_report(df):
    """
    Generate a data quality report
    """
    print("\n Data Quality Report")
    print("=" * 50)
    print(f"Total reviews: {len(df)}")
    print(f"Reviews per bank:\n{df['bank'].value_counts().to_string()}")
    print(f"\nRating distribution:\n{df['rating'].value_counts().sort_index().to_string()}")
    print(f"\nDate range: {df['date'].min()} to {df['date'].max()}")
    print(f"Missing dates: {df['date'].isna().sum()}")
    
    return {
        'total_reviews': len(df),
        'reviews_per_bank': df['bank'].value_counts().to_dict(),
        'rating_distribution': df['rating'].value_counts().sort_index().to_dict(),
        'date_range': {'min': df['date'].min(), 'max': df['date'].max()}
    }

if __name__ == "__main__":
 
    raw_df = pd.read_csv('data/raw/raw_reviews.csv')
    cleaned_df = preprocess_reviews(raw_df)
    save_cleaned_data(cleaned_df)

    generate_data_quality_report(cleaned_df)