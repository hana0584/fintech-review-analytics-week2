CREATE TABLE IF NOT EXISTS banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL UNIQUE,
    app_name VARCHAR(200)
);


INSERT INTO banks (bank_name, app_name) VALUES
    ('Commercial Bank of Ethiopia', 'CBE Mobile Banking'),
    ('Bank of Abyssinia', 'BOA Mobile'),
    ('Dashen Bank', 'Dashen Mobile Banking')
ON CONFLICT (bank_name) DO NOTHING;

CREATE TABLE IF NOT EXISTS reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INTEGER REFERENCES banks(bank_id),
    review_text TEXT NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review_date DATE,
    sentiment_label VARCHAR(10),
    sentiment_score DECIMAL(4,3),
    identified_theme VARCHAR(50),
    source VARCHAR(50) DEFAULT 'Google Play',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX idx_reviews_bank_id ON reviews(bank_id);
CREATE INDEX idx_reviews_date ON reviews(review_date);
CREATE INDEX idx_reviews_sentiment ON reviews(sentiment_label);
CREATE INDEX idx_reviews_theme ON reviews(identified_theme);


CREATE VIEW review_metrics AS
SELECT 
    b.bank_name,
    COUNT(r.review_id) as total_reviews,
    AVG(r.rating) as avg_rating,
    COUNT(CASE WHEN r.sentiment_label = 'positive' THEN 1 END) as positive_count,
    COUNT(CASE WHEN r.sentiment_label = 'negative' THEN 1 END) as negative_count,
    COUNT(CASE WHEN r.identified_theme = 'Performance & Crashes' THEN 1 END) as crash_complaints,
    COUNT(CASE WHEN r.identified_theme = 'Transactions & Transfers' THEN 1 END) as transfer_issues
FROM reviews r
JOIN banks b ON r.bank_id = b.bank_id
GROUP BY b.bank_name;