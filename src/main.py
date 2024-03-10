import argparse
import os
from typing import Any, Dict, List, Optional

import questionary as q
from loguru import logger

from cli_parser import process_variables
from generator import process_folder
from schemas import Var
from yaml_parser import PypyrusYamlParser


def run(source_dir, target_dir):
    yaml_file = os.path.join(source_dir, "pypyrus.yaml")
    pypyrus = PypyrusYamlParser(yaml_file)
    pypyrus.validate()
    data = pypyrus.get_data()

    try:
        user_inputs = process_variables(data)
        process_folder(source_dir, target_dir, user_inputs)
    except ValueError as err:
        logger.error(err)
        print(err)
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate files from a template using Pypyrus.")
    parser.add_argument("source", help="The source directory containing the pypyrus.yaml file.")
    parser.add_argument(
        "-t", "--target", help="The target directory where the generated files will be placed.", required=True
    )
    args = parser.parse_args()

    run(args.source, args.target)
