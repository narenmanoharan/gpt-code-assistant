import os
from datetime import datetime
from pathlib import Path
import toml

CONFIG_FILE_PATH = os.path.join(Path.home(), ".gpt-code-search/config.toml")

models = ["gpt-4-0613", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k"]


def create_default_config():
    default_config = {
        "model": "gpt-3.5-turbo-16k",
        "usage": {"query_count": 0, "last_updated": ""},
    }
    os.makedirs(os.path.dirname(CONFIG_FILE_PATH), exist_ok=True)
    with open(CONFIG_FILE_PATH, "w") as config_file:
        toml.dump(default_config, config_file)


def load_selected_model():
    config = toml.load(CONFIG_FILE_PATH)
    model = config.get("model")
    if model not in models:
        raise ValueError(
            f"Invalid model {model}. Valid models are {models}. "
            f"Please run `gpt-code-search select-model` to select a valid model."
        )
    return model


def write_selected_model(selected_model):
    config = {"model": selected_model}
    with open(CONFIG_FILE_PATH, "w") as config_file:
        toml.dump(config, config_file)


def load_config():
    with open(CONFIG_FILE_PATH, "r") as config_file:
        return toml.load(config_file)


def save_config(config):
    with open(CONFIG_FILE_PATH, "w") as config_file:
        toml.dump(config, config_file)


def update_usage_info():
    config = load_config()
    config["usage"]["query_count"] += 1
    config["usage"]["last_updated"] = datetime.utcnow().isoformat()
    save_config(config)
