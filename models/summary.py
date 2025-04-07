import mysql.connector
from groq import Groq

# Initialize the Groq client with your API key directly
client = Groq(api_key="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")

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
        return " ".join(reviews)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None

# Function to generate a summary using Groq
def generate_summary(text):
    if not text:
        return "No reviews available to summarize."
    
    # Updated prompt for clearer evaluation
    prompt = f"""Based on these customer reviews, provide a clear verdict on whether this fuel station is good or not:
    {text}
    
    First summarize the key positive and negative points in very brief bullet points.
    Then provide a final verdict - either "RECOMMENDED", "NOT RECOMMENDED", or "AVERAGE" along with a one-sentence explanation.
    Keep the entire response concise and direct.
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
    summary = chat_completion.choices[0].message.content
    return summary

# Main execution
if __name__ == "__main__":
    reviews_text = fetch_reviews()
    summary = generate_summary(reviews_text)
    print("\n📌 Fuel Station Verdict:")
    print(summary)
