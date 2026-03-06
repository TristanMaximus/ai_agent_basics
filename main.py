import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`
    verbose = args.verbose
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    print("Hello from ai-agent-basics!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("Error: Google Gemini API Key is not present!")
    gemini_client = genai.Client(api_key = api_key)
    gemini_response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents = messages,
        config = types.GenerateContentConfig(
            tools = [available_functions],
            system_instruction = system_prompt,
            temperature = 0
        )
    )
    usage_metadata = gemini_response.usage_metadata
    if usage_metadata != None:
        if args.verbose:
            print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
            print(f"Response tokens: {usage_metadata.candidates_token_count}")
    else:
        raise RuntimeError("Error: No Usage Metadata in Gemini response.")

    function_results = list()
    if gemini_response.function_calls != None:
        for function_call in gemini_response.function_calls:
            # printing info about a function that LLM decided to call
            print(function_call)
            print(f"Calling function: {function_call.name}({function_call.args})")

            # actually calling function and processing result
            function_call_result = call_function(function_call)
            if len(function_call_result.parts) == 0:
                raise RuntimeError(f"Error: something went wrong during the function call (no parts): {function_call.name}({function_call.args})")
            actual_func_response = function_call_result.parts[0].function_response
            if actual_func_response is None:
                raise RuntimeError(f"Error: something went wrong during the function call (no function response object): {function_call.name}({function_call.args})")
            if actual_func_response.response is None:
                raise RuntimeError(f"Error: something went wrong during the function call (no response in function response object): {function_call.name}({function_call.args})")
            function_results.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(gemini_response.text)


if __name__ == "__main__":
    main()
