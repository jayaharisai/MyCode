from .utils import (
    is_email,
    is_blank
    )

def input_validation(
        input: str,
        email:bool = None
        ) -> tuple[str, bool]:
    # String validation
    if is_blank(input): return "String is empty", False
    if email:
        result = is_email(input)
        if not result: return "Not a valid email id", False
    return "Successfully verified", True