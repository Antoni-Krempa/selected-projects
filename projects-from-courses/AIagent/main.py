import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions,call_function
import sys

def main():


    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("api_key bad")

    
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for i in range(20):

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents = messages,                                                     
            config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt)
        )

        if response.usage_metadata is None:
            raise RuntimeError("usage metadata is None")
        
        
        if response.candidates != None:
            for candidate in response.candidates:
                messages.append(candidate)

        


        if args.verbose:
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if not response.function_calls:
            print(response.text)
            return

        calls = response.function_calls
        if calls != None:
            results = []
            for call in calls:
                function_call_result = call_function(call,args.verbose)
                if function_call_result.parts == []:
                    raise Exception("empty .parts")
                    
                if function_call_result.parts[0].function_response == None:
                    raise Exception(".function_response problem")
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception(".response is None somehow")
                    


                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

                results.append(function_call_result.parts[0])

        messages.append(types.Content(role="user", parts=results))
        if i == 19:
            print("Error: Model did not produce a final response after maximum iterations.")
            sys.exit(1)


    


if __name__ == "__main__":
    main()
