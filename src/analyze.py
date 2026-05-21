import pandas as pd
from sentiment import analyze_reviews_with_vader
from thematic import extract_keywords_tfidf, assign_themes

def run_full_analysis():
    print("Starting Full Analysis Pipeline")
    try:
        df = pd.read_csv('data/cleaned_reviews.csv')
        print(f"Loaded {len(df)} reviews")
    except FileNotFoundError:
        print("data/cleaned_reviews.csv not found. Run src/preprocess.py first.")
        return None
    print("Step 1: Sentiment Analysis")
    sentiments, scores = analyze_reviews_with_vader(df)
    df['sentiment_label'] = sentiments
    df['sentiment_score'] = scores
    print("Step 2: Thematic Analysis")
    df = assign_themes(df)
    df.to_csv('data/analyzed_reviews.csv', index=False)
    print("Results saved to data/analyzed_reviews.csv")
    print("Summary Statistics")
    sentiment_by_bank = pd.crosstab(df['bank'], df['sentiment_label'])
    print(sentiment_by_bank)
    theme_by_bank = pd.crosstab(df['bank'], df['identified_theme'])
    print(theme_by_bank)
    print("Top Keywords per Bank")
    for bank in df['bank'].unique():
        keywords = extract_keywords_tfidf(df, bank, n_keywords=5)
        print(f"{bank}:")
        if keywords:
            for kw, score in keywords:
                print(f"  {kw} ({score:.3f})")
        else:
            print("  (no keywords)")
    return df

if __name__ == "__main__":
    run_full_analysis()