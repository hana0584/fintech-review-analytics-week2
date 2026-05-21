import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import os


DB_CONFIG = {
    'host': 'localhost',
    'database': 'bank_reviews',
    'user': 'postgres',
    'password': 'hana123',  
    'port': 5432
}

def get_connection():
    """Create database connection"""
    return psycopg2.connect(**DB_CONFIG)

def create_tables():
    """Create tables using schema.sql"""
    conn = get_connection()
    cursor = conn.cursor()
    
    with open('scripts/schema.sql', 'r') as f:
        schema_sql = f.read()
        cursor.execute(schema_sql)
    
    conn.commit()
    cursor.close()
    conn.close()
    print(" Tables created successfully")

def get_bank_id(cursor, bank_name):
    """Helper function to get bank_id from bank name"""
    cursor.execute("SELECT bank_id FROM banks WHERE bank_name = %s", (bank_name,))
    result = cursor.fetchone()
    return result[0] if result else None

def load_reviews_to_db(df):
    """
    Load analyzed reviews to PostgreSQL database
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    
    bank_ids = {}
    for bank in df['bank'].unique():
        cursor.execute("SELECT bank_id FROM banks WHERE bank_name = %s", (bank,))
        result = cursor.fetchone()
        if result:
            bank_ids[bank] = result[0]
    
    
    inserted_count = 0
    for _, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT INTO reviews 
                (bank_id, review_text, rating, review_date, 
                 sentiment_label, sentiment_score, identified_theme, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                bank_ids.get(row['bank']),
                row['review'],
                int(row['rating']),
                row['date'],
                row.get('sentiment_label', 'neutral'),
                float(row.get('sentiment_score', 0.5)),
                row.get('identified_theme', 'Other'),
                'Google Play'
            ))
            inserted_count += 1
        except Exception as e:
            print(f"Error inserting review: {e}")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"Inserted {inserted_count} reviews into database")
    return inserted_count

def verify_data():
    """Run verification queries"""
    conn = get_connection()
    cursor = conn.cursor()
    
    print("\n🔍 Data Verification")
    print("=" * 40)
    
    
    cursor.execute("""
        SELECT b.bank_name, COUNT(r.review_id) 
        FROM reviews r 
        JOIN banks b ON r.bank_id = b.bank_id 
        GROUP BY b.bank_name
    """)
    print("\nReviews per bank:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} reviews")
  
    cursor.execute("""
        SELECT b.bank_name, ROUND(AVG(r.rating), 2) 
        FROM reviews r 
        JOIN banks b ON r.bank_id = b.bank_id 
        GROUP BY b.bank_name
    """)
    print("\nAverage rating per bank:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} stars")
    
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN review_text IS NULL THEN 1 ELSE 0 END) as null_review,
            SUM(CASE WHEN rating IS NULL THEN 1 ELSE 0 END) as null_rating
        FROM reviews
    """)
    row = cursor.fetchone()
    print(f"\nData completeness:")
    print(f"  Total reviews: {row[0]}")
    print(f"  Null reviews: {row[1]}")
    print(f"  Null ratings: {row[2]}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
 
    df = pd.read_csv('data/analyzed_reviews.csv')
    
    create_tables()
    load_reviews_to_db(df)
    verify_data()