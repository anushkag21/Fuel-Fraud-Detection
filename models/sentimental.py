import mysql.connector
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np

# Load sentiment model
# Load model directly
from transformers import AutoTokenizer, AutoModelForSequenceClassification
tokenizer = AutoTokenizer.from_pretrained("citizenlab/twitter-xlm-roberta-base-sentiment-finetunned")
model = AutoModelForSequenceClassification.from_pretrained("citizenlab/twitter-xlm-roberta-base-sentiment-finetunned")

# Function to fetch reviews from MySQL
def fetch_reviews():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="new_password",
            database="fuel"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT user_review FROM review")
        reviews = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return reviews
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None

# Function to analyze sentiment
def analyze_sentiment(reviews):
    if not reviews:
        return {"positive": 0, "neutral": 0, "negative": 0}
    
    sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
    
    for review in reviews:
        # Tokenize and process input
        inputs = tokenizer(review, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            output = model(**inputs)
        
        # Get sentiment prediction
        scores = output.logits.softmax(dim=-1).numpy()[0]
        sentiment = np.argmax(scores)  # 0 = Negative, 1 = Neutral, 2 = Positive
        
        if sentiment == 0:
            sentiment_counts["negative"] += 1
        elif sentiment == 1:
            sentiment_counts["neutral"] += 1
        else:
            sentiment_counts["positive"] += 1
    
    return sentiment_counts

# Main execution
if __name__ == "__main__":
    reviews = fetch_reviews()
    if reviews:
        sentiment_results = analyze_sentiment(reviews)
        print("\nSentiment Analysis Results:")
        print(f"🔴 Negative: {sentiment_results['negative']}")
        print(f"🟡 Neutral: {sentiment_results['neutral']}")
        print(f"🟢 Positive: {sentiment_results['positive']}")
    else:
        print("No reviews found.")
