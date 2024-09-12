import json
import os
import logging
from sentiment import SentimentAnalyzer
from tools import execute_function
from ai_utils import chat_with_ai, summarize_conversation

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

sentiment_analyzer = SentimentAnalyzer()

# Load tool definitions from JSON file
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
json_path = os.path.join(project_root, 'resource', 'tool_definitions.json')

try:
    with open(json_path, 'r') as f:
        tool_definitions = json.load(f)
        toolscollection = tool_definitions['toolscollection']
except FileNotFoundError:
    logger.error(f"Tool definitions file not found at {json_path}")
    raise
except json.JSONDecodeError:
    logger.error(f"Invalid JSON in tool definitions file at {json_path}")
    raise

def main():
    print("Chat with TeamFire Agent (type 'bye' to exit)")
    conversation_history = [
        {"role": "system", "content": "You are an AI assistant that helps people find information."}
    ]

    while True:
        client_input = input("You: ")
        if client_input.lower() == 'bye':
            print("Goodbye!")
            break

        label, score = sentiment_analyzer.analyze(client_input)
        print(f"Sentiment: {label} (score: {score:.2f})")

        ai_message = chat_with_ai(client_input, conversation_history, toolscollection, label, score)
        
        if "tool_calls" in ai_message:
            for tool_call in ai_message["tool_calls"]:
                function_name = tool_call["function"]["name"]
                function_args = json.loads(tool_call["function"]["arguments"])
                function_response = execute_function(function_name, function_args)
                
                conversation_history.append({
                    "role": "assistant",
                    "content": ai_message["content"],
                    "tool_calls": ai_message["tool_calls"]
                })
                conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "name": function_name,
                    "content": function_response
                })
            
            ai_message = chat_with_ai("", conversation_history, toolscollection, label, score)
        
        print(f"AI: {ai_message['content']}")
        conversation_history.append({"role": "assistant", "content": ai_message['content']})

        if "speak to an advisor" in client_input.lower() or "talk to an advisor" in client_input.lower():
            print("Certainly! I'll connect you with a human advisor. Let me summarize our conversation for them.")
            summary = summarize_conversation(conversation_history)
            print("\nHere's a summary of our conversation that will be sent to the human advisor:")
            print(summary)
            
            # Create an appointment by adding the summary
            appointment_response = json.loads(execute_function("createAppointment", {"casedata": summary}))
            print(f"\nAppointment created with ID: {appointment_response['appointment_id']}")
            print("A human advisor will be with you. Thank you!")
            break

if __name__ == "__main__":
    main()