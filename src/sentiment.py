import pandas as pd
import numpy as np
from transformers import pipeline
from tqdm import tqdm
import time

class SentimentAnalyzer:
    def __init__(self):
        """
        Initialize the sentiment analyzer using DistilBERT
        """
        print("🤖 Loading sentiment analysis model...")
        self.classifier = pipeline(
            'sentiment-analysis',
            model='distilbert-base-uncased-finetuned-sst-2-english'
        )
        print("✅ Model loaded successfully")
    
    def analyze_single(self, text):
        """
        Analyze sentiment of a single text
        """
        if not text or len(text.strip()) == 0:
            return 'neutral', 0.5
        
        try:
            
            if len(text) > 500:
                text = text[:500]
            
            result = self.classifier(text)
            label = result[0]['label'].lower()  
            score = result[0]['score']
            
            
            if label == 'positive' and score > 0.80:
                return 'positive', score
            elif label == 'negative' and score > 0.70:
                return 'negative', score
            else:
                return 'neutral', score
                
        except Exception as e:
            print(f"Error analyzing text: {e}")
            return 'neutral', 0.5
    
    def analyze_batch(self, texts, batch_size=32):
        """
        Analyze sentiment for multiple texts
        """
        sentiments = []
        scores = []
        
        for i in tqdm(range(0, len(texts), batch_size), desc="Analyzing sentiment"):
            batch = texts[i:i+batch_size]
            batch_sentiments = []
            batch_scores = []
            
            for text in batch:
                sentiment, score = self.analyze_single(text)
                batch_sentiments.append(sentiment)
                batch_scores.append(score)
            
            sentiments.extend(batch_sentiments)
            scores.extend(batch_scores)
            time.sleep(0.1) 
        
        return sentiments, scores

def analyze_reviews_with_vader(df):
    """
    Alternative: Use VADER for faster sentiment analysis
    """
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    import nltk
    nltk.download('vader_lexicon', quiet=True)
    
    sia = SentimentIntensityAnalyzer()
    
    sentiments = []
    scores = []
    
    for text in tqdm(df['review'], desc="Analyzing with VADER"):
        vs = sia.polarity_scores(str(text))
        compound = vs['compound']
        scores.append(abs(compound))
        
        if compound >= 0.05:
            sentiments.append('positive')
        elif compound <= -0.05:
            sentiments.append('negative')
        else:
            sentiments.append('neutral')
    
    return sentiments, scores