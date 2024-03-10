from typing import Any, Dict, List, Optional

import questionary as q
from loguru import logger

from cli_parser import process_variables
from schemas import Var
from yaml_parser import PypyarusYamlParser
from generator import process_folder


def run(yaml_file):
    pypyrus = PypyarusYamlParser(yaml_file)
    pypyrus.validate()
    data = pypyrus.get_data()

    try:
        user_inputs = process_variables(data)
        print("User inputs:", user_inputs)
        process_folder("my_test/", "target_folder", user_inputs)
    except ValueError as err:
        logger.error(err)
        print(err)
        return


if __name__ == "__main__":
    run("my_test/pypyrus.yaml")
