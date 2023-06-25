import logging
import os

import typer
from rich.console import Console
from rich.logging import RichHandler

from core.ai import chat_completions
from core.config import (
    write_selected_model,
    update_usage_info,
    CONFIG_FILE_PATH,
    create_default_config,
)

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
def select_model():
    """
    Select the GPT model to use.
    """
    models = ["gpt-4-0613", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k"]
    console.print("Available Models:")
    for index, model in enumerate(models, start=1):
        console.print(f"{index}. {model}")

    selected_model = typer.prompt("Select a model (enter the number)")
    if selected_model.isdigit() and int(selected_model) in range(1, len(models) + 1):
        selected_model_name = models[int(selected_model) - 1]
        console.print(f"Selected model: {selected_model_name}")
        write_selected_model(selected_model_name)
    else:
        console.print("Invalid selection. Please enter a valid number.")
        typer.Exit()


@app.command()
def create_alias():
    """
    Instructions for creating an alias to gpt-code-search query.
    """
    console.print(
        "To create an alias, you need to edit your shell's configuration file. "
        "Here are instructions for Bash and Zsh (the most common shells)."
    )
    console.print(
        "\nIf you use Bash, run the following command:\n"
        "echo \"alias gq='gpt-code-search query'\" >> ~/.bashrc && source ~/.bashrc",
        style="bold green",
    )
    console.print(
        "\nIf you use Zsh, run the following command:\n"
        "echo \"alias gq='gpt-code-search query'\" >> ~/.zshrc && source ~/.zshrc",
        style="bold green",
    )
    console.print(
        "\nAfter running the appropriate command, you can use 'gq' as a shortcut for 'gpt-code-search query'."
    )
    typer.Exit()


@app.command()
def query(message: str):
    """
    Query the current directory with any questions.
    """
    if not check_openai_key():
        return

    response = chat_completions(message)
    update_usage_info()
    console.print(response)
    typer.Exit()


@app.callback()
def callback():
    if not os.path.exists(CONFIG_FILE_PATH):
        logging.info("Creating default config file...")
        create_default_config()

    console.print(
        "\nTip: Mention specific file names in your query for the best results. "
        "Run this CLI closer to the directory or file path for faster file tree searches. The max depth is 5 levels.\n",
        style="bold yellow",
    )


if __name__ == "__main__":
    app()
