import boto3

# Define AWS region
REGION = "us-east-1"

# Create an STS client to assume roles
sts_client = boto3.client("sts", region_name=REGION)

# Assume the user role to get temporary security credentials
assumed_user_role = sts_client.assume_role(
    RoleArn="arn:aws:iam::941377111974:role/User", 
    RoleSessionName="UserSession"
)

# Get temporary credentials from assumed role
creds = assumed_user_role["Credentials"]

# Initialize S3 client with temporary credentials
s3_client = boto3.client(
    "s3",
    region_name=REGION,
    aws_access_key_id=creds["AccessKeyId"],
    aws_secret_access_key=creds["SecretAccessKey"],
    aws_session_token=creds["SessionToken"]
)

# Define the S3 bucket name
bucket_name = "fang-demo-bucket"
total_size = 0

# List objects with prefix "assignment"
response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix="assignment")

if "Contents" in response:
    for obj in response["Contents"]:
        total_size += obj["Size"]
    print(f"Total size of 'assignment' files in '{bucket_name}': {total_size} bytes")
else:
    print(f"No 'assignment' files found in '{bucket_name}'.")
