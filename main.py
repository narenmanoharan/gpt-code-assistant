import logging
import os
import readline

import typer
from rich import print
from rich.console import Console

from core.ai import chat_completions

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = typer.Typer()
console = Console()

CONFIG_FILE_PATH = os.path.expanduser("~/.wolfia_codex")

readline.parse_and_bind('tab: complete')


@app.command()
def query():
    """
    Query the current directory with any questions.
    """
    query = typer.prompt("Query")
    response = chat_completions(query)
    print(response)


if __name__ == '__main__':
    console = Console()
    app()
