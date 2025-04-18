import re
import os
from faker import Faker
from tqdm import tqdm
import csv
import polars as pl
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
    

def generate_fake_data_csv(filename: str, num_rows: int, headers: list):
    fake = Faker()
    
    file_exists = os.path.exists(filename)
    write_header = not file_exists or os.stat(filename).st_size == 0

    # If file exists and has data, check header match
    if file_exists and not write_header:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            existing_headers = next(csv.reader(file))
            if existing_headers != headers:
                print("❌ Headers do not match. Data will not be inserted.")
                return

    # Now write (append) data with progress bar
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        if write_header:
            writer.writerow(headers)

        print(f"\n📦 Generating {num_rows} rows of fake data:")
        for _ in tqdm(range(num_rows), desc="Progress", unit="row"):
            row = [generate_value_by_header(fake, h) for h in headers]
            writer.writerow(row)

    print("✅ Done! Data successfully added.\n")

def generate_value_by_header(fake, header):
    header = header.lower()

    if "first name" in header:
        return fake.first_name()
    if "last name" in header:
        return fake.last_name()
    if "full name" in header or "name" in header:
        return fake.name()
    if "username" in header:
        return fake.user_name()
    if "password" in header:
        return fake.password()
    if "email" in header:
        return fake.email()
    if "phone" in header:
        return fake.phone_number()
    if "date of birth" in header:
        return fake.date_of_birth().isoformat()
    if "gender" in header:
        return fake.random_element(elements=("Male", "Female", "Other"))

    # Address
    if "street" in header:
        return fake.street_address()
    if "city" in header:
        return fake.city()
    if "state" in header:
        return fake.state()
    if "zip" in header:
        return fake.zipcode()
    if "country" in header:
        return fake.country()
    if "latitude" in header:
        return str(fake.latitude())
    if "longitude" in header:
        return str(fake.longitude())

    # Company
    if "company name" in header:
        return fake.company()
    if "job title" in header:
        return fake.job()
    if "department" in header:
        return fake.bs()
    if "website" in header:
        return fake.url()

    # Finance
    if "credit card number" in header:
        return fake.credit_card_number()
    if "credit card type" in header:
        return fake.credit_card_provider()
    if "credit card expiration" in header:
        return fake.credit_card_expire()
    if "iban" in header:
        return fake.iban()
    if "bank name" in header:
        return fake.bank()
    if "currency" in header:
        return fake.currency_code()
    if "bitcoin" in header:
        return fake.cryptocurrency_address()

    # Tech
    if "ip address" in header:
        return fake.ipv4()
    if "ipv6" in header:
        return fake.ipv6()
    if "mac address" in header:
        return fake.mac_address()
    if "domain" in header:
        return fake.domain_name()
    if "url" in header:
        return fake.url()
    if "user agent" in header:
        return fake.user_agent()
    if "browser" in header:
        return fake.chrome()
    if "operating system" in header:
        return fake.linux_platform_token()

    # Product
    if "product name" in header:
        return fake.word().title()
    if "price" in header:
        return f"${fake.pydecimal(left_digits=2, right_digits=2, positive=True)}"
    if "ean" in header:
        return fake.ean13()
    if "color" in header:
        return fake.color_name()
    if "category" in header:
        return fake.random_element(elements=("Electronics", "Clothing", "Books", "Toys"))

    # Date & Time
    if "date" in header and "time" not in header:
        return fake.date()
    if "datetime" in header:
        return fake.date_time().isoformat()
    if "time" in header:
        return fake.time()
    if "timezone" in header:
        return fake.timezone()

    # Misc
    if "uuid" in header:
        return fake.uuid4()
    if "license plate" in header:
        return fake.license_plate()
    if "file name" in header:
        return fake.file_name()
    if "hex color" in header:
        return fake.hex_color()
    if "emoji" in header:
        return fake.emoji()
    if "language" in header:
        return fake.language_name()
    if "country code" in header:
        return fake.country_code()

    # Default fallback
    return "N/A"

headers = [
    # Personal Information
    "First Name", "Last Name", "Full Name", "Username", "Password",
    "Email", "Phone Number", "Date of Birth", "Gender",
    # Address Information
    "Street Address", "City", "State", "Zip Code", "Country",
    "Latitude", "Longitude",
    # Company / Work Info
    "Company Name", "Job Title", "Department", "Company Email",
    "Work Phone", "Website",
    # Financial Info
    "Credit Card Number", "Credit Card Type", "Credit Card Expiration",
    "IBAN", "Bank Name", "Currency", "Bitcoin Address",
    # Internet / Tech
    "IP Address", "IPv6 Address", "MAC Address", "Domain Name",
    "URL", "User Agent", "Browser", "Operating System",
    # Product / Commerce
    "Product Name", "Price", "EAN-13 Barcode", "Color", "Category",
    # Dates & Time
    "Date", "DateTime", "Time", "Timezone",
    # Miscellaneous
    "UUID", "License Plate", "File Name", "Hex Color", "Emoji",
    "Language", "Country Code"
]

def is_csv_file(filename: str) -> bool:
    return filename.lower().strip().endswith('.csv')


def reading_csv_file(file_name: str):
    df = pl.read_csv(file_name)
    return df