import json
import logging

import openai
import requests
from rich.markdown import Markdown

from core.functions import (
    MAX_DEPTH,
    enabled_functions,
    get_contents_of_file,
    get_file_tree,
    search_codebase,
    truncate_text_to_token_limit,
)

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
            timeout=180,
        )
        return response
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred during ChatCompletion request: {http_err}")
        logging.error(f"Response content: {response.content}")
        return http_err
    except Exception as e:
        logging.error(
            "Unable to generate ChatCompletion response due to the following exception:"
        )
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

    if function_name == "get_file_tree":
        function_call = get_file_tree
        start_path = function_args.get("start_path")
        max_depth = function_args.get("max_depth") or MAX_DEPTH
        function_response = function_call(start_path, int(max_depth))
    elif function_name == "get_contents_of_file":
        function_call = get_contents_of_file
        file_path = function_args.get("path")
        function_response = function_call(file_path)
    elif function_name == "search_codebase":
        function_call = search_codebase
        keywords = function_args.get("keywords")
        start_path = function_args.get("start_path") or "."
        max_depth = function_args.get("max_depth") or MAX_DEPTH
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


content = """\
You're a GPT-4 powered coding assistant. Your role involves helping users understand and navigate their codebases,
providing assistance across a range of tasks.

You have access to two primary functions:
- `get_file_tree(start_path, max_depth)`: This function retrieves the project's file structure.
- `get_contents_of_file(path)`: This function fetches the contents of a given file.
- `search_codebase(keywords, start_path, max_depth)`: This function searches the codebase for a given keyword.

Leverage these tools to help with debugging, creating documentation, answering code-related queries, and generating
code snippets in line with the project's existing style and conventions.

Before answering any questions, always perform a search of the codebase or file tree. Aim to review at least five
different files before providing an answer and make sure to reference the most relevant file.

Your function calls are capped at ten per session, so make judicious use of them. If a 'readme.md' file exists, it can
serve as a starting point for high-level queries. If it doesn't, rely on file names and content to gather the necessary
information.

When composing your responses, use markdown for clarity and include code where necessary. Always aim for thorough,
complete answers, but if you're unsure, it's better to admit it rather than providing incorrect information.
"""


def chat_completions(query: str):
    while True:
        functions = enabled_functions()
        messages = [
            {
                "role": "system",
                "content": content,
            },
            {"role": "user", "content": query},
        ]

        response = chat_completion_request(messages, functions)
        max_recursion = 10
        counter = 0

        while response is not None and counter < max_recursion:
            response = get_next_completion(response, messages, functions)
            counter += 1

        return Markdown(messages[-1]["content"])
