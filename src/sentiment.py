import pandas as pd
from tqdm import tqdm

def analyze_reviews_with_vader(df):
    print("Running VADER sentiment analysis")
    try:
        from nltk.sentiment.vader import SentimentIntensityAnalyzer
        import nltk
        try:
            nltk.data.find('sentiment/vader_lexicon.zip')
        except LookupError:
            nltk.download('vader_lexicon', quiet=False)
        sia = SentimentIntensityAnalyzer()
        sentiments = []
        scores = []
        for text in tqdm(df['review'], desc="Analyzing"):
            text_str = str(text)
            if not text_str.strip():
                sentiments.append('neutral')
                scores.append(0.5)
                continue
            vs = sia.polarity_scores(text_str)
            compound = vs['compound']
            confidence = abs(compound)
            if compound >= 0.05:
                sentiments.append('positive')
            elif compound <= -0.05:
                sentiments.append('negative')
            else:
                sentiments.append('neutral')
            scores.append(confidence)
        return sentiments, scores
    except ImportError:
        print("nltk not installed. Run pip install nltk")
        return ['neutral'] * len(df), [0.5] * len(df)
    except Exception as e:
        print(f"VADER analysis failed: {e}")
        return ['neutral'] * len(df), [0.5] * len(df)

if __name__ == "__main__":
    test_df = pd.DataFrame({
        'review': [
            "This app is fantastic, fast and reliable!",
            "Terrible experience, keeps crashing every time.",
            "It's okay, nothing special."
        ]
    })
    sentiments, scores = analyze_reviews_with_vader(test_df)
    for i, (rev, sent, sc) in enumerate(zip(test_df['review'], sentiments, scores)):
        print(f"{i+1}. {rev} -> {sent} ({sc:.3f})")