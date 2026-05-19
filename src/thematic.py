import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import spacy


nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])

def preprocess_text_for_tfidf(text):
    """
    Preprocess text for TF-IDF extraction
    """
    doc = nlp(text.lower())
    
    
    tokens = [token.lemma_ for token in doc 
              if not token.is_stop 
              and not token.is_punct 
              and token.pos_ in ['NOUN', 'PROPN', 'ADJ']]
    
    return ' '.join(tokens)

def extract_keywords_tfidf(df, bank_name, n_keywords=10):
    """
    Extract top keywords for a specific bank using TF-IDF
    """
  
    bank_reviews = df[df['bank'] == bank_name]['review'].tolist()
    
    if len(bank_reviews) < 10:
        return []
    
    # Preprocess
    processed_reviews = [preprocess_text_for_tfidf(str(review)) for review in bank_reviews]
    
    
    vectorizer = TfidfVectorizer(
        max_features=50,
        ngram_range=(1, 2),
        stop_words='english'
    )
    
    try:
        tfidf_matrix = vectorizer.fit_transform(processed_reviews)
        
      
        feature_names = vectorizer.get_feature_names_out()
        avg_scores = np.array(tfidf_matrix.mean(axis=0)).flatten()
        
    
        top_indices = avg_scores.argsort()[-n_keywords:][::-1]
        keywords = [(feature_names[i], avg_scores[i]) for i in top_indices]
        
        return keywords
    except:
        return []

def perform_topic_modeling(df, bank_name, n_topics=5):
    """
    Perform LDA topic modeling to discover themes
    """
    from sklearn.feature_extraction.text import CountVectorizer
    
    # Filter reviews
    bank_reviews = df[df['bank'] == bank_name]['review'].tolist()
    
    if len(bank_reviews) < 20:
        return []
    
    # Create document-term matrix
    vectorizer = CountVectorizer(
        max_features=100,
        stop_words='english',
        ngram_range=(1, 2)
    )
    
    dtm = vectorizer.fit_transform(bank_reviews)
    
    # Run LDA
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(dtm)
    
    # Get topic keywords
    feature_names = vectorizer.get_feature_names_out()
    topics = []
    
    for topic_idx, topic in enumerate(lda.components_):
        top_indices = topic.argsort()[-5:][::-1]
        keywords = [feature_names[i] for i in top_indices]
        topics.append({
            'topic_id': topic_idx,
            'keywords': keywords
        })
    
    return topics

def assign_themes(df):
    """
    Assign themes to each review based on keywords
    """
    
    theme_keywords = {
        'Performance & Crashes': ['crash', 'freeze', 'slow', 'loading', 'timeout', 'error'],
        'Login & Authentication': ['login', 'password', 'fingerprint', 'face id', 'auth', 'biometric'],
        'Transactions & Transfers': ['transfer', 'send', 'money', 'payment', 'transaction', 'failed'],
        'User Interface & Design': ['ui', 'design', 'interface', 'menu', 'layout', 'look'],
        'Customer Support': ['support', 'help', 'customer service', 'complaint', 'assist'],
        'Feature Request': ['wish', 'suggest', 'add', 'feature', 'improve', 'implement'],
        'Security & OTP': ['otp', 'sms', 'code', 'secure', 'security', 'verification']
    }
    
    def get_theme(text):
        text_lower = str(text).lower()
        for theme, keywords in theme_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return theme
        return 'Other'
    
    df['identified_theme'] = df['review'].apply(get_theme)
    return df