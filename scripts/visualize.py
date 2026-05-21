import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import numpy as np


plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("Set2")

def plot_sentiment_distribution(df):
    """
    Create stacked bar chart of sentiment by bank
    """
    sentiment_counts = pd.crosstab(df['bank'], df['sentiment_label'])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sentiment_counts.plot(kind='bar', stacked=True, ax=ax, color=['#ff6b6b', '#ffd93d', '#6bcb77'])
    
    ax.set_title('Sentiment Distribution by Bank', fontsize=14, fontweight='bold')
    ax.set_xlabel('Bank')
    ax.set_ylabel('Number of Reviews')
    ax.legend(title='Sentiment')
    ax.tick_params(axis='x', rotation=0)
    
    
    for container in ax.containers:
        ax.bar_label(container)
    
    plt.tight_layout()
    plt.savefig('docs/sentiment_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_rating_distribution(df):
    """
    Create boxplot of ratings by bank
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    
    means = df.groupby('bank')['rating'].mean().sort_values()
    
    sns.boxplot(data=df, x='bank', y='rating', ax=ax, palette='Set2')
    ax.set_title('Rating Distribution by Bank', fontsize=14, fontweight='bold')
    ax.set_xlabel('Bank')
    ax.set_ylabel('Rating (1-5 stars)')
    
    
    for i, (bank, mean_val) in enumerate(means.items()):
        ax.text(i, mean_val + 0.1, f'Mean: {mean_val:.2f}', 
                ha='center', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('docs/rating_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_theme_frequency(df):
    """
    Create horizontal bar chart of theme frequency by bank
    """
    theme_counts = pd.crosstab(df['bank'], df['identified_theme'])
    
    
    theme_totals = theme_counts.sum().sort_values(ascending=False)
    theme_counts = theme_counts[theme_totals.index]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    theme_counts.T.plot(kind='barh', ax=ax)
    
    ax.set_title('Theme Frequency by Bank', fontsize=14, fontweight='bold')
    ax.set_xlabel('Number of Reviews')
    ax.set_ylabel('Theme')
    ax.legend(title='Bank')
    
    plt.tight_layout()
    plt.savefig('docs/theme_frequency.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_sentiment_trend(df):
    """
    Create sentiment trend over time
    """
    
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M')
    
    
    monthly_sentiment = df.groupby(['month', 'sentiment_label']).size().unstack(fill_value=0)
    monthly_sentiment_pct = monthly_sentiment.div(monthly_sentiment.sum(axis=1), axis=0)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    monthly_sentiment_pct.plot(kind='area', stacked=True, ax=ax, 
                                color=['#ff6b6b', '#ffd93d', '#6bcb77'], alpha=0.7)
    
    ax.set_title('Sentiment Trend Over Time', fontsize=14, fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Proportion of Reviews')
    ax.legend(title='Sentiment', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.set_ylim(0, 1)
    
    plt.tight_layout()
    plt.savefig('docs/sentiment_trend.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_wordcloud(df, bank_name):
    """
    Create word cloud for a specific bank
    """
    bank_reviews = ' '.join(df[df['bank'] == bank_name]['review'].tolist())
    
    wordcloud = WordCloud(width=800, height=400, background_color='white', 
                         max_words=100, colormap='viridis').generate(bank_reviews)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(f'Common Words in {bank_name} Reviews', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'docs/wordcloud_{bank_name.replace(" ", "_")}.png', dpi=300, bbox_inches='tight')
    plt.show()

def generate_insights(df):
    """
    Generate business insights from the data
    """
    print("\n" + "="*60)
    print("BUSINESS INSIGHTS REPORT")
    print("="*60)
    
    for bank in df['bank'].unique():
        bank_df = df[df['bank'] == bank]
        print(f"\n {bank}")
        print("-" * 40)
        
      
        avg_rating = bank_df['rating'].mean()
        sentiment_counts = bank_df['sentiment_label'].value_counts()
        
        print(f"Average Rating: {avg_rating:.2f} stars")
        print(f"Sentiment: {sentiment_counts.get('positive', 0)} positive, "
              f"{sentiment_counts.get('negative', 0)} negative, "
              f"{sentiment_counts.get('neutral', 0)} neutral")
        
       
        top_themes = bank_df['identified_theme'].value_counts().head(3)
        print("\nTop 3 Themes:")
        for theme, count in top_themes.items():
            print(f"  • {theme}: {count} reviews")
        
       
        pain_points = bank_df[(bank_df['sentiment_label'] == 'negative')]['identified_theme'].value_counts().head(2)
        print("\n Key Pain Points:")
        for theme, count in pain_points.items():
            print(f"  • {theme}: {count} complaints")
        
       
        drivers = bank_df[(bank_df['sentiment_label'] == 'positive')]['identified_theme'].value_counts().head(2)
        print("\n Satisfaction Drivers:")
        for theme, count in drivers.items():
            print(f"  • {theme}: {count} positive mentions")
        
       
        print("\n Example User Complaints:")
        complaints = bank_df[bank_df['sentiment_label'] == 'negative']['review'].head(3).tolist()
        for i, complaint in enumerate(complaints, 1):
            print(f"  {i}. \"{complaint[:100]}...\"")

if __name__ == "__main__":
    
    df = pd.read_csv('data/analyzed_reviews.csv')
    
 
    print("Generating visualizations...")
    plot_sentiment_distribution(df)
    plot_rating_distribution(df)
    plot_theme_frequency(df)
    
    
    for bank in df['bank'].unique():
        create_wordcloud(df, bank)
   
    generate_insights(df)