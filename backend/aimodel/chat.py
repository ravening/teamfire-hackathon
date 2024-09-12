import requests
import json
from sentiment import SentimentAnalyzer

# API Key and endpoint staff here
API_KEY = "184d81fd91524465a04f92da38d4222b"
ENDPOINT = "https://teamfireopenapi.openai.azure.com/openai/deployments/teamfiredeployment01/chat/completions?api-version=2024-02-15-preview"

sentiment_analyzer = SentimentAnalyzer()

def chat_with_ai(client_input):
    
    # Get the score of input
    label, score = sentiment_analyzer.analyze(client_input)
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }

    # Adding sentiment label on client input and send to model
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are an AI assistant that helps people find information. Consider the user's sentiment in your response."
            },
            {
                "role": "user",
                "content": f"User input (Sentiment: {label} with score {score:.2f}): {client_input}"
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
        return "Problem with request :/"

def main():
    print("Chat with TeamFire Agent (type 'bye' to exit)")
    while True:
        client_input = input("You: ")
        if client_input.lower() == 'bye':
            print("Goodbye!")
            break
        label, score = sentiment_analyzer.analyze(client_input)
        print(f"Sentiment: {label} (score: {score:.2f})")
        ai_response = chat_with_ai(client_input)
        print(f"AI: {ai_response}")

if __name__ == "__main__":
    main()