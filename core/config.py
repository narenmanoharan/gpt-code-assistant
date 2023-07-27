import os
import uuid
from pathlib import Path

import toml

from ai import open_ai

BASE_DIR = os.path.join(Path.home(), ".gpt-code-assistant")

CONFIG_FILE_PATH = os.path.join(BASE_DIR, ".gpt-code-assistant/config.toml")


def create_or_update_with_default_config():
    default_config = {
        "id": str(uuid.uuid4()),
        "model": "gpt-3.5-turbo-16k",
        "max_tokens": 14_000,
    }

    existing_config = {}
    if os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, "r") as config_file:
            existing_config = toml.load(config_file)
    for key, default_value in default_config.items():
        if key not in existing_config:
            existing_config[key] = default_value
        elif isinstance(default_value, dict):
            for subkey, subvalue in default_value.items():
                if subkey not in existing_config[key]:
                    existing_config[key][subkey] = subvalue
    os.makedirs(os.path.dirname(CONFIG_FILE_PATH), exist_ok=True)
    with open(CONFIG_FILE_PATH, "w") as config_file:
        toml.dump(existing_config, config_file)


def load_selected_model():
    config = load_config()
    selected_model = config.get("model")
    models = [model["name"] for model in open_ai.get_available_models()]
    if selected_model not in models:
        raise ValueError(
            f"Invalid model {selected_model}. Valid models are {models}. "
            f"Please run `gpt-code-assistant select-model` to select a valid model."
        )
    return selected_model


def load_max_tokens():
    config = load_config()
    return config.get("max_tokens")


def unique_id():
    config = load_config()
    return config["id"]


def save_selected_model(selected_model, selected_model_max_tokens):
    config = {"model": selected_model, "max_tokens": selected_model_max_tokens}
    with open(CONFIG_FILE_PATH, "w") as config_file:
        toml.dump(config, config_file)


def load_config():
    create_or_update_with_default_config()
    with open(CONFIG_FILE_PATH, "r") as config_file:
        return toml.load(config_file)


def save_config(config):
    with open(CONFIG_FILE_PATH, "w") as config_file:
        toml.dump(config, config_file)
