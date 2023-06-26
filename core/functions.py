import logging
import os
from typing import List, Union, Tuple

import tiktoken
from sklearn.feature_extraction.text import TfidfVectorizer

IGNORED_FOLDERS = [
    "__pycache__",
    ".git",
    ".idea",
    ".vscode",
    "venv",
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


def get_file_tree(start_path: str = ".", max_depth: int = MAX_DEPTH, depth: int = 0) -> list:
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


def search_codebase(keywords: List[str], max_depth: int = MAX_DEPTH) -> List[Tuple[str, float]]:
    """
    Search the codebase for a given list of keywords using TF-IDF vectorizer.
    The file path is given additional weight in the score calculation.
    :param keywords: The list of keywords to search for.
    :param max_depth: The maximum depth of the search.
    :return: A list of tuples where each tuple contains a file path and a TF-IDF score.
             Files with a higher TF-IDF score are ranked higher.
    """
    file_tree = get_file_tree(".", max_depth)
    documents = []
    PATH_WEIGHT = 10
    keywords = [keyword.lower() for keyword in keywords]

    for file_path in file_tree:
        try:
            with open(file_path, "r", errors="ignore") as file:
                contents = file.read()
            weighted_path = " ".join([file_path for _ in range(PATH_WEIGHT)])
            documents.append(weighted_path + " " + contents)
        except Exception:
            logging.error("Error reading file: {}".format(file_path))

    logging.info("Searching for keywords: {}".format(keywords))

    vectorizer = TfidfVectorizer(vocabulary=keywords, stop_words="english", max_features=100000)
    tfidf_matrix = vectorizer.fit_transform(documents)
    scores = tfidf_matrix.sum(axis=1)

    file_scores = [(file_path, score) for file_path, score in zip(file_tree, scores)]
    file_scores.sort(key=lambda x: x[1], reverse=True)

    logging.info("Found {} matching files.".format(len(file_scores)))
    return file_scores


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


def count_tokens(text) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode_ordinary(str(text)))


def truncate_text_to_token_limit(data: Union[str, List[str], List[Tuple[str, float]]], max_tokens: int) -> str:
    """
    Truncate the text (or list of strings or list of tuples) to fit within the maximum token limit.
    :param data: The text or list of strings or list of tuples to truncate.
    :param max_tokens: The maximum number of tokens.
    :return: The truncated data.
    """
    if isinstance(data, str):
        truncated_data = data
    elif isinstance(data, list):
        if all(isinstance(i, tuple) and len(i) == 2 for i in data):
            truncated_data = ", ".join(f"({text}, {value})" for text, value in data)
        elif all(isinstance(i, str) for i in data):
            truncated_data = " ".join(data)
        else:
            raise ValueError("Invalid data type. Expected str, list of str, or list of tuples (str, float).")
    else:
        raise ValueError("Invalid data type. Expected str, list of str, or list of tuples (str, float).")

    while count_tokens(truncated_data) > max_tokens:
        truncated_data = truncated_data[:-1]

    return truncated_data


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
            "description": "Search the codebase for a given list of keywords and return ranked matches based on a "
            "TF-IDF  scoring. Files with a keyword in the path are given additional weight in scoring "
            "than files with a keyword in the content.",
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
                            "type": "number",
                            "description": "TF-IDF score of the match. Higher score means more relevant to the "
                            "keywords.",
                        },
                    },
                },
                "description": "List of file paths and TF-IDF scores, sorted by score in descending order.",
            },
            "parameters": {
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "The list of keywords to search for. Format: ['keyword1', 'keyword2']. Please "
                        "provide at least three keywords.",
                    },
                },
                "required": ["keywords"],
            },
        },
        {
            "name": "get_file_tree",
            "description": "Get the file tree of the project based on the current working directory.",
            "returns": {
                "type": "array",
                "items": {
                    "type": "string",
                    "description": "The path to a file in the file tree.",
                },
                "description": "List of file paths in the file tree.",
            },
            "parameters": {
                "type": "object",
                "properties": {
                    "start_path": {
                        "type": "string",
                        "description": "The path to start the search from. Defaults to the current directory.",
                        "default": ".",
                    },
                },
                "required": ["start_path"],
            },
        },
    ]
