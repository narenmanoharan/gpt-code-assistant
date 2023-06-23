import json
import logging

import openai
import requests
from rich.markdown import Markdown

from core.functions import get_file_tree, get_contents_of_file, enabled_functions


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
        "max_tokens": 4_000,
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
    function_args = json.loads(assistant_message["function_call"]["arguments"])

    if function_name == 'get_file_tree':
        function_call = get_file_tree
        start_path = function_args.get('start_path')
        max_depth = int(function_args.get('max_depth'))
        function_response = function_call(start_path, max_depth)
    elif function_name == 'get_contents_of_file':
        function_call = get_contents_of_file
        file_path = function_args.get('path')
        function_response = function_call(file_path)
    else:
        raise ValueError(f"Function {function_name} not found.")

    messages.append(
        {
            "role": "function",
            "name": function_name,
            "content": str(function_response),
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
             "content": "You are a incredible coding assistant who is helping people understand codebases and help people with question that they have about the behaviour of code. You will look up the necessary files using the functions provided and answers relevant questions only based on the context. Use the functions to access the file tree of the project or the contents of a file using the functions provided!!! You can use the file tree to answer any high level questionssuch as 'What does this project do?' or 'What is the purpose of this project?'You can use the contents of a file to answer any low level questions such as 'What is the purpose of the function foo?' or 'What is the purpose of the class bar?'You have access to the following functions: get_file_tree(start_path, max_depth), get_contents_of_file(path).get_contents_of_file(path) returns the contents of a file as a string.  Always look up the file tree in the first function call before answering any question!!! You can keep calling functions a maximum of 10 times. So look up as many files as you need to answer the question. You can also use the files you have already looked up. Don't look up the same file twice. If you do, you will be penalized. Try to look up at least 5 files in separate function calls before answering a question. Always use the most relevant file to answer the question. If you don't, you will be penalized. If the file is not found, try to look up the file tree again and then look up a different file. If you still are not confident, please say 'I don't know'. So use the functions to look up the files!!! Please provide code when necessary and use markdown for the answer."},
            {"role": "user", "content": query}]

        response = chat_completion_request(messages, functions)
        max_recursion = 10
        counter = 0

        while response is not None and counter < max_recursion:
            response = get_next_completion(response, messages, functions)
            counter += 1

        return Markdown(messages[-1]["content"])
