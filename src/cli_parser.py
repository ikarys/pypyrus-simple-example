from typing import Any, Dict

import questionary as q
from icecream import ic
from loguru import logger

from schemas import Var


def evaluate_condition(condition: Dict[str, Any], user_inputs: Dict[str, Any]) -> bool:
    """
    Evaluate a condition based on user inputs.

    Args:
        condition (Dict[str, Any]): A dictionary containing the condition to evaluate, with the following keys:
            - source (str): The name of the user input to evaluate.
            - operator (str): The comparison operator to use. Must be one of "==", "!=", "<", "<=", ">", or ">=".
            - value: The value to compare the user input to.
        user_inputs (Dict[str, Any]): A dictionary containing the user inputs.

    Returns:
        bool: True if the condition is met, False otherwise.

    Raises:
        ValueError: If the operator is not a valid comparison operator.
    """
    source = condition.get("source")
    operator = condition.get("operator")
    value = condition.get("value")

    if source not in user_inputs:
        return False

    match operator:
        case "eq":
            return user_inputs[source] == value
        case "ne":
            return user_inputs[source] != value
        case "lt":
            return user_inputs[source] < value
        case "lte":
            return user_inputs[source] <= value
        case "gt":
            return user_inputs[source] > value
        case "gte":
            return user_inputs[source] >= value
        case "in":
            return value in user_inputs[source]
        case "nin":
            return value not in user_inputs[source]
        case _:
            raise ValueError(f"`{operator}` Invalid operator for condition")


def prompt_user_for_input(variable: Dict) -> Any:
    input_text = variable.get("input")
    default_value = variable.get("default", None)
    choices = variable.get("choices", None)
    required = variable.get("required", False)

    if choices is not None:
        # Convert bool choices to strings
        str_choices = [str(c) for c in choices]

        choices_prompt = q.select(
            f"{input_text}:",
            choices=str_choices,
            default=str(default_value),
        ).ask()

        # Convert string choice back to bool if necessary
        if isinstance(choices[0], bool):
            return choices[str_choices.index(choices_prompt)]
        else:
            return choices_prompt
    else:
        input_prompt = q.text(
            f"{input_text}:",
            default=str(default_value if default_value is not None else ""),
            validate=lambda text: True if (len(text) > 0 or required is False) else "Please enter a value",
        ).ask()
        return input_prompt.strip()


def process_variables(data: Dict[str, Var]) -> Dict[str, Any]:
    user_inputs = {}

    for var_name, var in data.items():
        conditions = var.get("conditions", None)
        if conditions is not None:
            if not all(evaluate_condition(c, user_inputs) for c in conditions):
                continue

        user_inputs[var_name] = prompt_user_for_input(var)

    return user_inputs
