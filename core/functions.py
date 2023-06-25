import logging
import os
import re
from typing import List, Union, Tuple

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


def search_codebase(keywords: List[str], max_depth: int = 5) -> List[Tuple[str, int]]:
    """
    Search the codebase for a given list of keywords.
    :param keywords: The list of keywords to search for.
    :param max_depth: The maximum depth of the search.
    :return: A list of tuples where each tuple contains a file path and a rank.
             Files with a keyword in the path are ranked higher than files with a keyword in the content.
    """
    file_tree = get_file_tree(".", max_depth)
    matching_files = {}

    for file_path in file_tree:
        try:
            rank = 0
            with open(file_path, "r", errors="ignore") as file:
                contents = file.read()

            if any(re.search(keyword, contents, re.IGNORECASE) for keyword in keywords):
                rank = 1

            if any(
                re.search(keyword, file_path, re.IGNORECASE) for keyword in keywords
            ):
                rank = 2

            if rank > 0:
                matching_files[file_path] = rank
        except Exception:
            logging.error("Error reading file: {}".format(file_path))

    logging.info("Searching for keywords: {}".format(keywords))
    logging.info("Found {} matching files.".format(len(matching_files)))
    matching_files = sorted(matching_files.items(), key=lambda x: x[1], reverse=True)
    return matching_files


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


def truncate_text_to_token_limit(
    data: Union[str, List[str], List[Tuple[str, int]]], max_tokens: int
):
    """
    Truncate the text (or list of strings or list of tuples) to fit within the maximum token limit.
    :param data: The text or list of strings or list of tuples to truncate.
    :param max_tokens: The maximum number of tokens.
    :return: The truncated text or list of strings or list of tuples.
    """
    if not data:
        return []

    if isinstance(data, str):
        chunks = data.split(" ")
    elif isinstance(data, list):
        if data and isinstance(data[0], tuple):
            chunks = [item[0] for item in data]
        else:
            chunks = data
    else:
        raise ValueError(
            "The input data should be a string or a list of strings or a list of tuples."
        )

    total_tokens = sum(len(chunk.split(" ")) for chunk in chunks)

    while total_tokens > max_tokens:
        total_tokens -= len(chunks[-1].split(" "))
        chunks = chunks[:-1]

    if isinstance(data, str):
        return " ".join(chunks)
    elif data and isinstance(data[0], tuple):
        ranks = [item[1] for item in data[: len(chunks)]]
        return list(zip(chunks, ranks))
    else:
        return chunks


def enabled_functions():
    return [
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
            "description": "Search the codebase for a given list of keywords and return ranked matches. Files with a "
            "keyword in the path are ranked higher than files with a keyword in the content.",
            "returns": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path to the file.",
                        },
                        "rank": {
                            "type": "integer",
                            "description": "Rank of the match. 2 if keyword found "
                            "in file path, 1 if keyword found in file content.",
                        },
                    },
                },
                "description": "List of file paths and ranks, sorted by rank in descending order.",
            },
            "parameters": {
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "The list of keywords to search for. Format: ['keyword1', 'keyword2']",
                    },
                    "max_depth": {
                        "type": "integer",
                        "description": "The maximum depth of the search.",
                        "default": 5,
                    },
                },
                "required": ["keywords"],
            },
        },
    ]
