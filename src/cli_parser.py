from typing import Any, Dict, Optional

import questionary as q
from loguru import logger

from schemas import Var


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
        logger.debug(required)
        input_prompt = q.text(
            f"{input_text}:",
            default=str(default_value if default_value is not None else ""),
            validate=lambda text: True if (len(text) > 0 or required is False) else "Please enter a value",
        ).ask()
        return input_prompt.strip()


def process_variables(data: Dict[str, Var]) -> Dict[str, Any]:
    user_inputs = {}

    for var_name, var in data.items():
        if getattr(var, "condition", None) is not None:
            conditions = var.condition

            if conditions is not None:
                conditions_met = all(
                    c.source in user_inputs and eval(f"user_inputs['{c.source}'] {c.operator} {repr(c.value)}")
                    for c in conditions
                )

                if not conditions_met:
                    continue

        user_inputs[var_name] = prompt_user_for_input(var)

    return user_inputs
