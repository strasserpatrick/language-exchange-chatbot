import os

import yaml
from dotenv import load_dotenv
from pydantic import BaseSettings


class OpenaiConfig(BaseSettings):
    model: str
    role: str


class StreamlitConfig(BaseSettings):
    start_message: str
    placeholder_message: str


class TerraformConfig(BaseSettings):
    resource_group_name: str
    location: str


class DockerConfig(BaseSettings):
    image_name: str
    registry_name: str


class Config(BaseSettings):
    openai: OpenaiConfig
    streamlit: StreamlitConfig
    terraform: TerraformConfig
    docker: DockerConfig


def read_config(config_path: str):
    # Read the YAML file
    with open(config_path, "r") as f:
        yaml_config = yaml.safe_load(f)

        # Parse the YAML into Config
        return Config.parse_obj(yaml_config)


load_dotenv()
config_path = os.environ.get("CONFIG_FILE", "config.yaml")
config: Config = read_config(config_path)
