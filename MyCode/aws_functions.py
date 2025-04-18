from .utils import (
    validate_aws_keys_with_access_check
    )

def aws_key_validation(
        access_key_id: str,
        secret_access_key: str
    ):
    message, result = validate_aws_keys_with_access_check(
        access_key_id, secret_access_key
    )
    if result: return message, True
    return message, False