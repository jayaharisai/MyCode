from .utils import (
    is_email,
    is_blank, generate_fake_data_csv, headers,
    is_csv_file, reading_csv_file
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

# Generate some syntactic data
def syntactic_data_generator(
        file_name: str,
        rows: int,
        required_headers: list = None
) -> tuple[str, bool]:
    if not is_csv_file(file_name): return "Not a csv extension", False
    if not required_headers: return "Headers can't be empty", False
    for head in required_headers:
        if head not in headers: return f"{head} not in {headers}", False
    result = generate_fake_data_csv(file_name, rows, required_headers)
    return "Successfully Generated", True

def read_csv(file_name: str):
    data = reading_csv_file(file_name)
    return data