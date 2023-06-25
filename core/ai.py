import json
import logging

import openai
import requests
from rich.markdown import Markdown

from core.functions import get_file_tree, get_contents_of_file, enabled_functions, truncate_text_to_token_limit, \
    search_codebase, MAX_DEPTH

# Reduced from 16k to 14k to allow for prompt context
MAX_TOKENS = 14_000


def chat_completion_request(messages, functions=None, model="gpt-3.5-turbo-16k"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    json_data = {
        "model": model,
        "messages": messages,
        "functions": functions or [],
        "function_call": "auto",
        "temperature": 0,
    }
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
            timeout=180
        )
        return response
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred during ChatCompletion request: {http_err}")
        logging.error(f"Response content: {response.content}")
        return http_err
    except Exception as e:
        logging.error("Unable to generate ChatCompletion response due to the following exception:")
        logging.error(f"Exception: {e}")
        return e


def get_next_completion(previous_response, messages, functions):
    assistant_message = previous_response.json()["choices"][0]["message"]
    messages.append(assistant_message)

    if assistant_message.get("function_call") is None:
        return None

    function_name = assistant_message["function_call"]["name"]
    try:
        function_args = json.loads(assistant_message["function_call"]["arguments"])
    except json.JSONDecodeError:
        return None

    if function_name == 'get_file_tree':
        function_call = get_file_tree
        start_path = function_args.get('start_path')
        max_depth = function_args.get('max_depth') or MAX_DEPTH
        function_response = function_call(start_path, int(max_depth))
    elif function_name == 'get_contents_of_file':
        function_call = get_contents_of_file
        file_path = function_args.get('path')
        function_response = function_call(file_path)
    elif function_name == 'search_codebase':
        function_call = search_codebase
        keywords = function_args.get('keywords')
        start_path = function_args.get('start_path') or '.'
        max_depth = function_args.get('max_depth') or MAX_DEPTH
        function_response = function_call(keywords, start_path, int(max_depth))
    else:
        raise ValueError(f"Function {function_name} not found.")

    truncated_response = truncate_text_to_token_limit(function_response, MAX_TOKENS)

    messages.append(
        {
            "role": "function",
            "name": function_name,
            "content": str(truncated_response),
        }
    )
    next_response = chat_completion_request(
        messages=messages,
        functions=functions,
    )
    return next_response


def chat_completions(query: str):
    while True:
        functions = enabled_functions()
        messages = [
            {"role": "system",
             "content": """You are an advanced coding assistant powered by GPT-4. Your task is to assist users in understanding and navigating their codebases, helping them with a variety of tasks, all based on the provided context.

You have access to two powerful functions: get_file_tree(start_path, max_depth) and get_contents_of_file(path). The former returns the project's file tree, while the latter retrieves the contents of a specified file.

Here are some common use-cases:

1. Debugging: Help users debug errors by finding the relevant files and code snippets.
2. Documentation: Generate well-structured documentation for large files or functionalities.
3. General Queries: Answer general questions about any part of the code.
4. Code Generation: Generate new code snippets that adhere to the existing project's style and conventions.

Remember, always lookup the file tree or search the codebase first, before answering any questions as the first step in answering any question. Create keywords from the question and search the codebase or user the file tree to find the most relevant file. 

For high level questions, you can use the 'readme.md' file as a starting point (if it exists). Else, look at the file names and contents to find the most relevant file. You can call functions a maximum of 10 times per session, so use your calls wisely. Try to lookup at least 5 different files before answering a question, and always reference the most relevant file.

Please provide code when necessary and use markdown for the answer. Be as detailed as possible, and try to provide a complete answer. But if you're unable to, it's okay to say 'I don't know'. Do not make up answers.
                """
             },
            {"role": "user", "content": query}]

        response = chat_completion_request(messages, functions)
        max_recursion = 10
        counter = 0

        while response is not None and counter < max_recursion:
            response = get_next_completion(response, messages, functions)
            counter += 1

        return Markdown(messages[-1]["content"])
