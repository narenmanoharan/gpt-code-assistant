import logging
import os

import typer
from rich.console import Console
from rich.logging import RichHandler

from core.ai import chat_completions

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)],
)

app = typer.Typer()
console = Console()


def check_openai_key():
    """
    Check if the OPENAI_API_KEY environment variable is set. If not, guide the user on where to find it.
    """
    if "OPENAI_API_KEY" not in os.environ:
        console.print(
            "Error: OPENAI_API_KEY is not set in your environment variables.",
            style="bold red",
        )
        console.print(
            "To find your API Key, go to: https://platform.openai.com/account/api-keys\n"
        )
        console.print(
            "Once you have the API Key, you can set it in your environment variables like this:"
        )
        console.print("export OPENAI_API_KEY='your_key'\n", style="bold green")
        return False
    return True


@app.command()
def query():
    """
    Query the current directory with any questions.
    """
    if not check_openai_key():
        return
    console.print(
        "\nTip: Mention specific file names in your query for the best results. "
        "Run this CLI closer to the directory or file path for faster file tree searches. The max depth is 5 levels.\n",
        style="bold yellow",
    )
    message = typer.prompt("Query")
    response = chat_completions(message)
    console.print(response)
    typer.Exit()


if __name__ == "__main__":
    app()
