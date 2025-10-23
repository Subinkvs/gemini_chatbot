from google import genai 
from google.genai.errors import APIError 
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 

try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except APIError as e:
    print(f"Error initializing client: {e}")
   

def chat_with_gemini(prompt: str) -> str:
    """
    Sends a prompt to the Gemini model and returns the response text.
    
    Args:
        prompt: The user's message.
        
    Returns:
        The model's response text, or an error message if the call fails.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt, 
        )
        
        return response.text.strip()
        
    except APIError as e:
        return f"An API error occurred: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == "__main__":
    if 'client' in locals() and client:
        print("Chatbot 🤖: Hello there! I’m your AI assistant powered by **Gemini**. What would you like to talk about today?\n")
        
        while True:
            user_input = input("You: ")
            
            if user_input.lower() in ["quit", "exit", "bye"]:
                print("Chatbot: Goodbye! 👋")
                break

            response = chat_with_gemini(user_input)
            print("Chatbot:", response)
    else:
        print("Chatbot initialization failed. Please check your API key and network connection.")