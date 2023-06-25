import logging
import os
import readline

import typer
from rich.console import Console
from rich import print
from termcolor import colored

from core.ai import chat_completions

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = typer.Typer()
console = Console()

CONFIG_FILE_PATH = os.path.expanduser("~/.wolfia_codex")

readline.parse_and_bind('tab: complete')


def check_openai_key():
    """
    Check if the OPENAI_API_KEY environment variable is set. If not, guide the user on where to find it.
    """
    if 'OPENAI_API_KEY' not in os.environ:
        print(colored("Error: OPENAI_API_KEY is not set in your environment variables.", 'red'))
        print("To find your API Key, go to: https://platform.openai.com/account/api-keys\n")
        print("Once you have the API Key, you can set it in your environment variables like this:")
        print(colored("export OPENAI_API_KEY='your_key'\n", 'green'))
        return False
    return True


@app.command()
def query():
    """
    Query the current directory with any questions.
    """
    if not check_openai_key():
        return
    query = typer.prompt("Query")
    response = chat_completions(query)
    print(response)


if __name__ == '__main__':
    console = Console()
    app()
