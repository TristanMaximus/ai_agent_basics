import os
from dotenv import load_dotenv
from google import genai

def main():
    print("Hello from ai-agent-basics!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("Error: Google Gemini API Key is not present!")
    gemini_client = genai.Client(api_key = api_key)
    gemini_response = gemini_client.models.generate_content(model="gemini-2.5-flash", contents = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")
    usage_metadata = gemini_response.usage_metadata
    if usage_metadata != None:
        print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
        print(f"Response tokens: {usage_metadata.candidates_token_count}")
    else:
        raise RuntimeError("Error: No Usage Metadata in Gemini response.")
    print(gemini_response.text)


if __name__ == "__main__":
    main()
