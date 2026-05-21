import pandas as pd
from src.sentiment import SentimentAnalyzer
from src.thematic import extract_keywords_tfidf, assign_themes, perform_topic_modeling

def run_full_analysis():
    """
    Run complete sentiment and thematic analysis pipeline
    """
    print("🚀 Starting Full Analysis Pipeline")
    print("=" * 50)
    
    
    df = pd.read_csv('data/cleaned_reviews.csv')
    print(f"Loaded {len(df)} reviews")
    

    print("\n Step 1: Sentiment Analysis")
    analyzer = SentimentAnalyzer()
    sentiments, scores = analyzer.analyze_batch(df['review'].tolist())
    df['sentiment_label'] = sentiments
    df['sentiment_score'] = scores
    
   
    print("\nStep 2: Thematic Analysis")
    df = assign_themes(df)
    
   
    df.to_csv('data/analyzed_reviews.csv', index=False)
    print("\n Results saved to data/analyzed_reviews.csv")
    
    print("\nSummary Statistics")
    print("-" * 30)
    
   
    sentiment_by_bank = pd.crosstab(df['bank'], df['sentiment_label'])
    print("\nSentiment by Bank:")
    print(sentiment_by_bank)
    
   
    theme_by_bank = pd.crosstab(df['bank'], df['identified_theme'])
    print("\nTheme by Bank:")
    print(theme_by_bank)
    
    print("\n🔑 Top Keywords per Bank")
    print("-" * 30)
    for bank in df['bank'].unique():
        keywords = extract_keywords_tfidf(df, bank, n_keywords=8)
        print(f"\n{bank}:")
        for kw, score in keywords:
            print(f"  - {kw} ({score:.3f})")
    
    return df

if __name__ == "__main__":
    df = run_full_analysis()