import boto3
from botocore.exceptions import ClientError

# Initialize IAM client
iam_client = boto3.client("iam")

# Define the username to be created
user_name = "userFang"

try:
    iam_client.create_user(UserName=user_name)
except ClientError as e:
    if e.response['Error']['Code'] == 'EntityAlreadyExists':
        print(f"IAM User {user_name} is already created.")
    else:
        raise
