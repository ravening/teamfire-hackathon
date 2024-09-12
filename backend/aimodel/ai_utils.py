import requests
import json
import time
import logging

logger = logging.getLogger(__name__)

API_KEY = "184d81fd91524465a04f92da38d4222b"
ENDPOINT = "https://teamfireopenapi.openai.azure.com/openai/deployments/teamfiredeployment01/chat/completions?api-version=2024-02-15-preview"

def chat_with_ai(client_input, conversation_history, toolscollection, sentiment_label, sentiment_score, max_retries=5, initial_retry_delay=1):
    # Send a message to the agent and get a response. 
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }

    messages = conversation_history + [
        {
            "role": "user",
            "content": f"User input (Sentiment: {sentiment_label} with score {sentiment_score:.2f}): {client_input}"
        }
    ]

    payload = {
        "messages": messages,
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 2000,
        "tools": toolscollection,
        "tool_choice": "auto"
    }

    # Added a retry mechanism for rate limiting but not sure how it works cuz found from internet.
    for attempt in range(max_retries):
        try:
            response = requests.post(ENDPOINT, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()['choices'][0]['message']
        except requests.RequestException as e:
            if response.status_code == 429:
                retry_delay = initial_retry_delay * (2 ** attempt)
                logger.warning(f"Rate limit exceeded. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error(f"Error: {e}")
                return {"content": f"I'm sorry, there was a problem with the request: {str(e)}"}
    
    return {"content": "Sorry man but limit is exceed already :( try again later)"}

# Summarize the conversation history
def summarize_conversation(conversation_history):
    summary_prompt = "Please provide a concise summary of the following conversation, highlighting key points, questions asked, and any important information shared:"
    for message in conversation_history:
        if message['role'] != 'system':
            summary_prompt += f"\n{message['role'].capitalize()}: {message['content']}"

    summary_messages = [
        {"role": "system", "content": "You are an AI assistant that summarizes conversations."},
        {"role": "user", "content": summary_prompt}
    ]

    summary_payload = {
        "messages": summary_messages,
        "temperature": 0.7,
        "max_tokens": 300
    }

    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }

    try:
        response = requests.post(ENDPOINT, headers=headers, json=summary_payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.RequestException as e:
        logger.error(f"Error in summarizing conversation: {e}")
        return "Unable to generate summary due to an error."