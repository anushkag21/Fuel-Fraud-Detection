import mysql.connector
from groq import Groq

# Initialize the Groq client with your API key directly
client = Groq(api_key="api key")

# Function to fetch and combine reviews
def fetch_reviews():
    try:
        # Database connection
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="fuel"
        )
        cursor = conn.cursor()
        # Fetch all reviews
        cursor.execute("SELECT user_review FROM review")
        reviews = [row[0] for row in cursor.fetchall()]
        # Close connection
        cursor.close()
        conn.close()
        return reviews  # Return list of individual reviews
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None

# Function to extract topics from reviews
def extract_topics(reviews):
    if not reviews:
        return "No reviews available for topic extraction."
    
    # Join all reviews for context
    all_reviews = " ".join(reviews)
    
    # Prompt for topic extraction
    prompt = f"""Extract the most common topics/themes mentioned in these fuel station reviews:
    {all_reviews}
    
    For each identified topic:
    1. Provide a short tag name (1-3 words)
    2. Show the percentage of reviews that mention this topic
    3. Include a brief 1-sentence sentiment summary for each topic
    
    Format as a JSON array of topics with fields: "tag", "percentage", "sentiment"
    Limit to the top 6-8 most significant topics.
    """
    
    # Call Groq API
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192"
    )
    
    # Get the response
    topics = chat_completion.choices[0].message.content
    return topics

# Function to provide an overall verdict
def generate_verdict(reviews):
    if not reviews:
        return "No reviews available for verdict."
    
    # Join all reviews for context
    all_reviews = " ".join(reviews)
    
    # Prompt for overall verdict
    prompt = f"""Based on these fuel station reviews, provide a clear verdict:
    {all_reviews}
    
    Give a simple "RECOMMENDED", "NOT RECOMMENDED", or "AVERAGE" rating followed by 
    a one-sentence explanation. Keep it very concise.
    """
    
    # Call Groq API
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192"
    )
    
    # Get the response
    verdict = chat_completion.choices[0].message.content
    return verdict

# Main execution
if __name__ == "__main__":
    reviews = fetch_reviews()
    
    print("\n🏷️ Key Topics:")
    topics = extract_topics(reviews)
    print(topics)
    
    print("\n📌 Overall Verdict:")
    verdict = generate_verdict(reviews)
    print(verdict)
