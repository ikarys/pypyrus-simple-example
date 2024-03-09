from typing import Any, Dict, List, Optional

import questionary as q
from loguru import logger

from cli_parser import process_variables
from schemas import Var
from yaml_parser import PypyarusYamlParser


def run(yaml_file):
    pypyrus = PypyarusYamlParser(yaml_file)
    pypyrus.validate()
    data = pypyrus.get_data()

    try:
        user_inputs = process_variables(data)
        print("User inputs:", user_inputs)
    except ValueError as e:
        print("Validation failed:", e)


if __name__ == "__main__":
    run("pypyrus.yaml")
