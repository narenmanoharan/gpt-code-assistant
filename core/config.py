import os
from datetime import datetime
from pathlib import Path

import toml

CONFIG_FILE_PATH = os.path.join(Path.home(), ".gpt-code-search/config.toml")

models = ["gpt-4-0613", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k"]


def create_or_update_with_default_config():
    default_config = {
        "model": "gpt-3.5-turbo-16k",
        "usage": {"query_count": 0, "last_updated": ""},
        "analytics": "enabled",
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
    model = config.get("model")
    if model not in models:
        raise ValueError(
            f"Invalid model {model}. Valid models are {models}. "
            f"Please run `gpt-code-search select-model` to select a valid model."
        )
    return model


def update_usage_info():
    if has_opted_out_of_analytics():
        return
    config = load_config()
    config["usage"]["query_count"] += 1
    config["usage"]["last_updated"] = datetime.utcnow().isoformat()
    save_config(config)


def save_opt_out_of_analytics():
    config = load_config()
    config["analytics"] = "disabled"
    save_config(config)


def has_opted_out_of_analytics():
    config = load_config()
    return config["analytics"] == "disabled"


def save_selected_model(selected_model):
    config = {"model": selected_model}
    with open(CONFIG_FILE_PATH, "w") as config_file:
        toml.dump(config, config_file)


def load_config():
    create_or_update_with_default_config()
    with open(CONFIG_FILE_PATH, "r") as config_file:
        return toml.load(config_file)


def save_config(config):
    with open(CONFIG_FILE_PATH, "w") as config_file:
        toml.dump(config, config_file)
