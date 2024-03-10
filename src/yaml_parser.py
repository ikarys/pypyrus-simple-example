from typing import Dict, Optional

import questionary as q
import yaml
from jinja2 import Environment
from loguru import logger

from schemas import PapyrusSchema, Var

env = Environment()


class PypyrusYamlParser:
    __user_inputs: Dict = {}
    __data: Dict[str, Var] = {}

    def __init__(self, yaml_file: str) -> None:
        self.yaml_file = yaml_file
        self.__load_yaml()

    def __load_yaml(self) -> None:
        with open(self.yaml_file, "r") as file:
            self.__data = yaml.safe_load(file)
        self.convert_simple_key()

    def convert_simple_key(self) -> None:
        for key, value in self.__data.items():
            if isinstance(value, str):
                self.__data[key] = dict(input=key, default=value)

    def validate(self) -> PapyrusSchema:
        try:
            return PapyrusSchema(vars=self.__data)
        except ValueError as err:
            logger.error("Validation failed:", err)
            raise err

    def get_data(self) -> Dict[str, Var]:
        return self.__data
