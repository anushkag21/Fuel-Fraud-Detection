from flask import Flask, jsonify, send_from_directory, request, redirect
import mysql.connector
from groq import Groq
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
import os

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key="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")

# Load sentiment model
model = AutoModelForSequenceClassification.from_pretrained("citizenlab/twitter-xlm-roberta-base-sentiment-finetunned")
tokenizer = AutoTokenizer.from_pretrained("citizenlab/twitter-xlm-roberta-base-sentiment-finetunned")

# Serve signup.html directly
@app.route('/')
def home():
    return send_from_directory('.', 'signup.html')  # Looks for signup.html in root

# Static file serving (JS, CSS, etc.)
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

# Fetch reviews from database
def fetch_reviews():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Aastha1811",
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

# Generate summary using Groq LLM
def generate_summary(reviews):
    if not reviews:
        return "No reviews available to summarize."
    
    prompt = f"""Summarize these fuel station reviews:
    {reviews}
    
    - Key positive and negative points
    - Final verdict: "RECOMMENDED", "NOT RECOMMENDED", or "AVERAGE"
    """
    
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192"
    )
    return response.choices[0].message.content

# Extract topics
def extract_topics(reviews):
    if not reviews:
        return "No reviews available for topic extraction."
    
    prompt = f"""Extract key themes from these reviews:
    {reviews}
    
    Format: JSON array with "tag", "percentage", "sentiment"
    Limit: Top 6-8 topics.
    """
    
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192"
    )
    return response.choices[0].message.content

# Generate verdict
def generate_verdict(reviews):
    if not reviews:
        return "No reviews available for verdict."
    
    prompt = f"""Provide a verdict for these reviews:
    {reviews}
    
    Verdict: "RECOMMENDED", "NOT RECOMMENDED", or "AVERAGE"
    Short explanation.
    """
    
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192"
    )
    return response.choices[0].message.content

# Analyze sentiment
def analyze_sentiment(reviews):
    if not reviews:
        return {"positive": 0, "neutral": 0, "negative": 0}
    
    sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
    
    for review in reviews:
        inputs = tokenizer(review, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            output = model(**inputs)
        
        scores = output.logits.softmax(dim=-1).numpy()[0]
        sentiment = np.argmax(scores)  # 0 = Negative, 1 = Neutral, 2 = Positive
        
        if sentiment == 0:
            sentiment_counts["negative"] += 1
        elif sentiment == 1:
            sentiment_counts["neutral"] += 1
        else:
            sentiment_counts["positive"] += 1
    
    return sentiment_counts

# Flask API routes
@app.route('/get_summary', methods=['GET'])
def get_summary():
    reviews = fetch_reviews()
    summary = generate_summary(" ".join(reviews)) if reviews else "No reviews found."
    return jsonify({"summary": summary})

@app.route('/generate_verdict', methods=['GET'])
def get_verdict():
    reviews = fetch_reviews()
    verdict = generate_verdict(" ".join(reviews)) if reviews else "No reviews found."
    return jsonify({"verdict": verdict})

@app.route('/analyze_sentiment', methods=['GET'])
def get_sentiment():
    reviews = fetch_reviews()
    sentiment = analyze_sentiment(reviews)
    return jsonify(sentiment)

@app.route('/extract_topics', methods=['GET'])
def get_topics():
    reviews = fetch_reviews()
    topics = extract_topics(" ".join(reviews)) if reviews else "No reviews found."
    return jsonify({"topics": topics})

if __name__ == '__main__':
    app.run(debug=True)
