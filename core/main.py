import logging
import os
from datetime import datetime

import typer
from rich.console import Console
from rich.logging import RichHandler

from core.ai import chat_completions
from core.config import (
    save_selected_model,
    log_usage_info,
    CONFIG_FILE_PATH,
    create_or_update_with_default_config,
    save_opt_out_of_analytics,
    configure_deps,
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
        console.print("To find your API Key, go to: https://platform.openai.com/account/api-keys\n")
        console.print("Once you have the API Key, you can set it in your environment variables like this:")
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
        save_selected_model(selected_model_name)
    else:
        console.print("Invalid selection. Please enter a valid number.")
        typer.Exit()


@app.command()
def query(message: str):
    """
    Query the current directory with any questions.
    """
    if not check_openai_key():
        return

    start_time = datetime.utcnow()
    response = chat_completions(message)
    end_time = datetime.utcnow()
    log_usage_info(start_time, end_time)
    console.print(response)
    typer.Exit()


@app.command()
def opt_out_of_analytics():
    """
    Opt out of anonymous usage analytics and crash reports.
    """
    save_opt_out_of_analytics()
    console.print("You have opted out of anonymous usage analytics and crash reports.")


@app.callback()
def callback():
    if not os.path.exists(CONFIG_FILE_PATH):
        logging.info("Creating default config file...")
        create_or_update_with_default_config()

    console.print(
        "\nTip: Mention specific file names in your query for the best results. "
        "Run this CLI closer to the directory or file for more accurate answers. The max depth is 5 levels.\n",
        style="bold yellow",
    )
    if not os.getenv("LOCAL_DEV"):
        configure_deps()


if __name__ == "__main__":
    app()
