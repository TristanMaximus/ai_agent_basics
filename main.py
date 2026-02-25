import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    # Now we can access `args.user_prompt`
    print("Hello from ai-agent-basics!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("Error: Google Gemini API Key is not present!")
    gemini_client = genai.Client(api_key = api_key)
    gemini_response = gemini_client.models.generate_content(model="gemini-2.5-flash", contents = messages)
    usage_metadata = gemini_response.usage_metadata
    if usage_metadata != None:
        print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
        print(f"Response tokens: {usage_metadata.candidates_token_count}")
    else:
        raise RuntimeError("Error: No Usage Metadata in Gemini response.")
    print(gemini_response.text)


if __name__ == "__main__":
    main()
