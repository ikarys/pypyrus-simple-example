from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ValidationError, field_validator, validator

class Condition:
    source: str
    operator: Literal["==", "!=", "<", "<=", ">", ">="]
    value: Any

class VarConditions(BaseModel):
    source: str
    operator: str
    value: Any

class Var(BaseModel):
    input: Optional[str]
    default: Optional[Any] = None
    required: Optional[bool] = True
    conditions: List[VarConditions] | None = None
    choices: Optional[List[Any]] = None

    @validator("choices")
    def validate_choices(cls, value, values):
        if value is not None and not isinstance(value, list):
            raise ValueError("Choices must be a list")

        if values.get("default") is not None and value is not None and values.get("default") not in value:
            raise ValueError("Default value must be in choices")

        return value

class PapyrusSchema(BaseModel):
    vars: Dict[str, Var]
