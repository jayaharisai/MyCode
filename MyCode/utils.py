import re
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

def is_email(input: str) -> bool:
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(email_regex, input))

def is_blank(input: str):
    return input is not None and input.strip() == ""

def validate_aws_keys_with_access_check(access_key_id, secret_access_key):
    try:
        session = boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key
        )
        s3_client = session.client('s3')
        s3_client.list_buckets()
        return "AWS keys are valid and have access.", True

    except (NoCredentialsError, PartialCredentialsError) as e:
        return "Invalid AWS credentials", False

    except ClientError as e:
        if e.response['Error']['Code'] == 'AccessDenied':
            return "AWS keys are valid but do not have sufficient permissions to perform the action.", True  
        return "Invalid AWS credentials",False