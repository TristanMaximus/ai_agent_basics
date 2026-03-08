import os
import sys
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

    for _ in range(20):
        if generate_content(gemini_client, messages, args.verbose):
            sys.exit()
    sys.exit(1)


def generate_content(client, messages, verbose):
    gemini_response = client.models.generate_content(
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
        if verbose:
            print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
            print(f"Response tokens: {usage_metadata.candidates_token_count}")
    else:
        raise RuntimeError("Error: No Usage Metadata in Gemini response.")

    # checking candidates and appending them if present to messages, to make sure model is aware of previous responses and uses them
    if gemini_response.candidates is not None:
        for candidate in gemini_response.candidates:
            messages.append(candidate.content)

    if not gemini_response.function_calls:
        print("Response:")
        print(gemini_response.text)
        return True

    function_results = list()
    for function_call in gemini_response.function_calls:
        # printing info about a function that LLM decided to call
        print(f"Calling function: {function_call.name}({function_call.args})")

        # actually calling function and processing result
        function_call_result = call_function(function_call)

        # handling bad results
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
            or not function_call_result.parts[0].function_response.response
        ):
            raise RuntimeError(f"Empty function response for {function_call.name}")

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

        function_results.append(function_call_result.parts[0])

    # after functions executed, append functions results to the messages for model to be aware of them on subsequent iterations
    messages.append(types.Content(role="user", parts=function_results))
    return False


if __name__ == "__main__":
    main()
