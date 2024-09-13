import requests
import json
import os
import logging
from azure.cosmos import CosmosClient, PartitionKey
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Configuration
API_KEY = os.environ.get('API_KEY')
ENDPOINT = os.environ.get('API_ENDPOINT')

COSMOS_DB_ENDPOINT = os.environ.get('ACCOUNT_HOST')
COSMOS_DB_KEY = os.environ.get('ACCOUNT_KEY')

COSMOS_DB_DATABASE_NAME = "ConversationDB"
COSMOS_DB_CONTAINER_NAME = "Conversations"

# Initialize Cosmos client
cosmos_client = CosmosClient(COSMOS_DB_ENDPOINT, COSMOS_DB_KEY)
database = cosmos_client.create_database_if_not_exists(id=COSMOS_DB_DATABASE_NAME)
container = database.create_container_if_not_exists(
    id=COSMOS_DB_CONTAINER_NAME,
    partition_key=PartitionKey(path="/conversation_id"),
    offer_throughput=400
)

def save_conversation(conversation_id, conversation):
    container.upsert_item({
        'id': conversation_id,
        'conversation_id': conversation_id,
        'messages': conversation
    })

def get_conversation(conversation_id):
    try:
        item_response = container.read_item(item=conversation_id, partition_key=conversation_id)
        return item_response['messages']
    except Exception as e:
        return []

def chat_with_ai(conversation_id, client_input):
    conversation = get_conversation(conversation_id)

    conversation.append({
        "role": "user",
        "content": client_input
    })

    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }

    payload = {
        "messages": conversation,
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 2000
    }

    for _ in range(5):  # Retry up to 5 times
        try:
            response = requests.post(ENDPOINT, headers=headers, json=payload)
            response.raise_for_status()
            ai_response = response.json()['choices'][0]['message']['content'].strip()

            conversation.append({
                "role": "assistant",
                "content": ai_response
            })
            save_conversation(conversation_id, conversation)

            return ai_response
        except requests.RequestException as e:
            if response.status_code == 429:
                print("Rate limit exceeded, waiting before retrying...")
                time.sleep(10)  # Wait for 10 seconds before retrying
            else:
                print(f"Error: {e}")
                return "I'm sorry, there is a problem with the request."
    return "I'm sorry, there is a problem with the request."
