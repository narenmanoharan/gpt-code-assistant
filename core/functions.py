import logging
import os
import re
from typing import List, Union

import tiktoken

IGNORED_FOLDERS = [
    "__pycache__",
    ".git",
    ".idea",
    "node_modules",
    ".bundle",
    ".gradle",
    "build",
    ".DS_Store",
    ".ipynb_checkpoints",
]
IGNORED_FILES = [
    "package-lock.json",
    ".env",
    "Gemfile.lock",
    "yarn.lock",
    "*.pyc",
    "local.properties",
    "*.xcodeproj",
    "*.xcworkspace",
    "*.csv",
    "*.xlsx",
    "*.json",
    ".bat",
]

MAX_DEPTH = 5


def get_file_tree(
    start_path: str = ".", max_depth: int = MAX_DEPTH, depth: int = 0
) -> list:
    """
    Get the file tree of the project based on the current working directory.
    :param start_path: The path to the directory to start the search from.
    :param max_depth: The maximum depth of the search.
    :param depth: The current depth of the search.
    :return: The file tree.
    """
    if depth > max_depth:
        return []
    tree = []
    for item in os.listdir(start_path):
        if item in IGNORED_FOLDERS or item in IGNORED_FILES:
            continue
        item_path = os.path.join(start_path, item)
        if os.path.isfile(item_path):
            tree.append(item_path)
        elif os.path.isdir(item_path):
            tree += get_file_tree(item_path, max_depth, depth + 1)
    return tree


def search_codebase(
    keywords: List[str], start_path: str = ".", max_depth: int = 5
) -> List[str]:
    """
    Search the codebase for a given list of keywords.
    :param keywords: The list of keywords to search for.
    :param start_path: The path to the directory to start the search from.
    :param max_depth: The maximum depth of the search.
    :return: A list of file paths that contain any of the keywords.
    """
    file_tree = get_file_tree(start_path, max_depth)
    matching_files = set()

    for file_path in file_tree:
        try:
            with open(file_path, "r", errors="ignore") as file:
                contents = file.read()

            if any(re.search(keyword, contents, re.IGNORECASE) for keyword in keywords):
                matching_files.add(file_path)
        except Exception:
            logging.error("Error reading file: {}".format(file_path))

    logging.info("Searching for keywords: {}".format(keywords))
    logging.info(
        "Found {} matching files in {}.".format(len(matching_files), start_path)
    )
    logging.info("Matching files: {}".format(matching_files))
    return list(matching_files)


def get_contents_of_file(file_path: str) -> str:
    """
    Get the contents of a file.
    :param file_path: The path to the file.
    :return: The contents of the file, or an empty string if the file is not found.
    """
    try:
        with open(file_path, "r") as file:
            logging.info("Reading file: {}".format(file_path))
            return file.read()
    except FileNotFoundError:
        return ""


def count_tokens(text: str) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode_ordinary(text))


def truncate_text_to_token_limit(text: Union[str, List[str]], max_tokens: int):
    """
    Truncate the text (or list of strings) to fit within the maximum token limit.
    :param text: The text or list of strings to truncate.
    :param max_tokens: The maximum number of tokens.
    :return: The truncated text or list of strings.
    """
    if isinstance(text, str):
        chunks = text.split(" ")
    elif isinstance(text, list):
        chunks = text
    else:
        raise ValueError("The input text should be a string or a list of strings.")

    total_tokens = sum(len(chunk.split(" ")) for chunk in chunks)

    while total_tokens > max_tokens:
        total_tokens -= len(chunks[-1].split(" "))
        chunks = chunks[:-1]

    if isinstance(text, str):
        return " ".join(chunks)
    else:
        return chunks


def enabled_functions():
    return [
        {
            "name": "get_file_tree",
            "description": "Get the file tree of the project based on the current working directory. "
            "Access the current project root, with (./)",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_path": {
                        "type": "string",
                        "description": "The path to the directory to start the search from.",
                        "default": ".",
                    },
                    "max_depth": {
                        "type": "string",
                        "description": "The maximum depth of the search."
                        "Use a max of {} since the search is very slow.".format(
                            MAX_DEPTH
                        ),
                    },
                    "depth": {
                        "type": "string",
                        "description": "The current depth of the search.",
                        "default": "0",
                    },
                },
                "required": ["start_path", "max_depth"],
            },
        },
        {
            "name": "get_contents_of_file",
            "description": "Get the contents of a file. Returns empty string if the file is not found.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The path to the file.",
                    },
                },
                "required": ["path"],
            },
        },
        {
            "name": "search_codebase",
            "description": "Search the codebase for a given list of keywords.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "The list of keywords to search for. Format: ['keyword1', 'keyword2']",
                    },
                    "start_path": {
                        "type": "string",
                        "description": "The path to the directory to start the search from.",
                        "default": ".",
                    },
                    "max_depth": {
                        "type": "string",
                        "description": "The maximum depth of the search.",
                        "default": "5",
                    },
                },
                "required": ["keywords"],
            },
        },
    ]
