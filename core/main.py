import logging
import os

import typer
from rich.console import Console
from rich.logging import RichHandler

from ai.open_ai import get_available_models, query_llm
from core.config import (CONFIG_FILE_PATH,
                         create_or_update_with_default_config,
                         save_selected_model)
from data.database import create_tables_if_not_exists
from repository import projects

logging.basicConfig(
    level=logging.ERROR,
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
    model_name = [model["name"] for model in get_available_models()]
    model_max_tokens = [model["max_tokens"] for model in get_available_models()]
    console.print("Available Models:")
    for index, model in enumerate(model_name, start=1):
        console.print(f"{index}. {model}")
    console.print("")

    model_index = typer.prompt("Select a model (enter the number)")
    if model_index.isdigit() and int(model_index) in range(1, len(model_name) + 1):
        selected_model_name = model_name[int(model_index) - 1]
        selected_max_tokens = model_max_tokens[int(model_index) - 1]
        console.print(f"Selected model: {selected_model_name}")
        save_selected_model(selected_model_name, selected_max_tokens)
    else:
        console.print("Invalid selection. Please enter a valid number.")


@app.command()
def query(project_name: str, query: str):
    """
    Query your codebase. Provide the project name (you can list all projects with `gpt-code-assistant list-projects`)
    """
    if not check_openai_key():
        return

    query_llm(project_name, query)


@app.command()
def create_project(name: str, path: str):
    """
    Create a new project for path or update the existing project and start indexing it.
    """
    absolute_path = os.path.abspath(path)
    if not os.path.exists(absolute_path):
        raise typer.BadParameter(f"Path {absolute_path} does not exist. Please enter a valid path.")
    projects.create_project(name, absolute_path)

@app.command()
def delete_project(name: str):
    """
    Delete a project and all its data (embeddings included)
    """
    projects.delete_project(name)


@app.command()
def refresh_project(name: str):
    """
    Trigger a reindex of a project and update the embeddings to the latest content.
    """
    projects.reindex_project(name)

@app.command()
def list_projects():
    """
    List all projects.
    """
    projects.list_all_projects()

@app.callback(invoke_without_command=True)
def callback(ctx: typer.Context):
    if not os.path.exists(CONFIG_FILE_PATH):
        console.print("Creating default config file...")
        create_or_update_with_default_config()

    create_tables_if_not_exists()

    if ctx.invoked_subcommand is None:
        typer.main.get_command(app).get_help(ctx)


if __name__ == "__main__":
    app()
