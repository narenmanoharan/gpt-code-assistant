import json
import logging

import openai
import requests
from rich.markdown import Markdown

from core.config import load_selected_model
from core.functions import (
    MAX_DEPTH,
    enabled_functions,
    get_contents_of_file,
    search_codebase,
    truncate_text_to_token_limit,
)

# Reduced from 16k to 14k to allow for prompt context
MAX_TOKENS = 14_000

PROMPT = """\
You're a incredible powered coding assistant. Your role is to help users understand and navigate their codebases,
providing assistance across a range of tasks.

You have access to three primary functions:
- `search_codebase(keywords, max_depth)`: Search the codebase for a keywords with rankings based on the file path
and contents. Higher ranking is better. Always use this function first. If there are no hits on a query, try some
different keywords similar to the query. (eg). use interceptor, if interceptors is not found.


- `get_contents_of_file(path)`: Fetch the contents of a file. Based on the answer from `search_codebase`, make a
judgement on the most relevant file and fetch the contents of that file. Read at least 5 files before answering my
calling this function multiple times. All the files should be different each time.

You have a total of 10 function calls. Use them wisely.

Use these tools to debug, create documentation, answer code-related queries, and generate code snippets
in line with the project's style. You will always use these functions before answering a question, particularly
`search_codebase`. You will not answer any questions without using these functions first. If you cannot find a
relevant file, say 'I don't know'. If you don't, you will be penalized.

Once you find relevant files with the file tree or search functions, always use `get_contents_of_file` to fetch the
contents of the file and review the contents of at least three files before answering.

Compose responses in markdown with code when necessary. Your objective is to provide the most accurate and detailed
answer possible, even if it results in a longer response. Let's start assisting with your coding tasks!
"""


def chat_completion_request(messages, functions=None):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    json_data = {
        "model": load_selected_model(),
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

    if function_name == "get_contents_of_file":
        function_call = get_contents_of_file
        file_path = function_args.get("path")
        function_response = function_call(file_path)
    elif function_name == "search_codebase":
        function_call = search_codebase
        keywords = function_args.get("keywords")
        max_depth = function_args.get("max_depth") or MAX_DEPTH
        function_response = function_call(keywords, int(max_depth))
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
            {
                "role": "system",
                "content": PROMPT,
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
