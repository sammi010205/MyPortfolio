import boto3
import os

REGION = "us-east-1"

# Assume Dev Role
sts_client = boto3.client("sts", region_name=REGION)

dev_role = sts_client.assume_role(
    RoleArn="arn:aws:iam::941377111974:role/Dev",  
    RoleSessionName="DevSession"
)

# Get temporary credentials
creds = dev_role["Credentials"]

# Create S3 client with assumed credentials
s3_client = boto3.client(
    "s3",
    region_name=REGION,
    aws_access_key_id=creds["AccessKeyId"],
    aws_secret_access_key=creds["SecretAccessKey"],
    aws_session_token=creds["SessionToken"]
)

bucket_name = "fang-demo-bucket"

# List and delete all objects
response = s3_client.list_objects_v2(Bucket=bucket_name)

if "Contents" in response:
    for obj in response["Contents"]:
        s3_client.delete_object(Bucket=bucket_name, Key=obj["Key"])
        print(f"Deleted: {obj['Key']}")

# Delete the bucket
s3_client.delete_bucket(Bucket=bucket_name)
print(f"Deleted bucket: {bucket_name}")

