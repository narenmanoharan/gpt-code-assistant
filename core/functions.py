import os


def get_file_tree(start_path: str, max_depth: int, depth: int = 0) -> dict:
    """
    Get the file tree of the project based on the current working directory.
    :param start_path: The path to the directory to start the search from.
    :param max_depth: The maximum depth of the search.
    :param depth: The current depth of the search.
    :return: The file tree.
    """
    if depth > max_depth:
        return {}
    tree = {}
    for item in os.listdir(start_path):
        item_path = os.path.join(start_path, item)
        if os.path.isfile(item_path):
            tree[item] = item_path
        elif os.path.isdir(item_path):
            tree[item] = get_file_tree(item_path, max_depth, depth + 1)
    return tree


def get_contents_of_file(file_path: str) -> str:
    """
    Get the contents of a file.
    :param file_path: The path to the file.
    :return: The contents of the file, or an empty string if the file is not found.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return ""


def enabled_functions():
    return [
        {
            "name": "get_file_tree",
            "description": "Get the file tree of the project based on the current working directory. Access the current project root, with (./)",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_path": {
                        "type": "string",
                        "description": "The path to the directory to start the search from."
                    },
                    "max_depth": {
                        "type": "string",
                        "description": "The maximum depth of the search. Use a max of 3 since the search is very slow.",
                    },
                    "depth": {
                        "type": "string",
                        "description": "The current depth of the search.",
                        "default": "0",
                    }
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
                        "description": "The path to the file."
                    },
                },
                "required": ["path"],
            }
        },
    ]
