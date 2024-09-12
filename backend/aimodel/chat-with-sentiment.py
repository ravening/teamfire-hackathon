import requests
import json
from transformers import pipeline

# Configuration
API_KEY = "184d81fd91524465a04f92da38d4222b"  # Make sure to fill in your API key
ENDPOINT = "https://teamfireopenapi.openai.azure.com/openai/deployments/teamfiredeployment01/chat/completions?api-version=2024-02-15-preview"

# Initialize sentiment analysis pipeline
sentiment_pipeline = pipeline("text-classification", model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")

def analyze_sentiment(text):
    result = sentiment_pipeline(text)[0]
    return result['label'], result['score']

def chat_with_ai(client_input):
    # Analyze sentiment
    sentiment_label, sentiment_score = analyze_sentiment(client_input)
    
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }

    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are an AI assistant that helps people find information. Consider the user's sentiment in your response."
            },
            {
                "role": "user",
                "content": f"User input (Sentiment: {sentiment_label} with score {sentiment_score:.2f}): {client_input}"
            }
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 800
    }

    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except requests.RequestException as e:
        print(f"Error: {e}")
        return "I'm sorry, because there is a problem with request"

def main():
    print("Chat with TeamFire Agent (type 'bye' to exit)")
    while True:
        client_input = input("You: ")
        if client_input.lower() == 'bye':
            print("Goodbye!")
            break
        
        sentiment_label, sentiment_score = analyze_sentiment(client_input)
        print(f"Sentiment: {sentiment_label} (score: {sentiment_score:.2f})")
        
        ai_response = chat_with_ai(client_input)
        print(f"AI: {ai_response}")

if __name__ == "__main__":
    main()