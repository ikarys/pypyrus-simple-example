from typing import Dict, Optional

import questionary as q
import yaml
from jinja2 import Environment
from loguru import logger

from schemas import PapyrusSchema, Var

env = Environment()


class PypyarusYamlParser:
    __user_inputs: Dict = {}
    __data: Dict[str, Var] = {}
    __schema: PapyrusSchema

    def __init__(self, yaml_file: str) -> None:
        self.yaml_file = yaml_file
        self.__load_yaml()

    def __load_yaml(self) -> None:
        with open(self.yaml_file, "r") as file:
            self.__data = yaml.safe_load(file)
        self.validate()

    def validate(self) -> None:
        try:
            self.__schema = PapyrusSchema(vars=self.__data)
        except ValueError as e:
            logger.error("Validation failed:", e)

    def get_data(self) -> Dict[str, Var]:
        return self.__data
