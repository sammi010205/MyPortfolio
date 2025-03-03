import boto3

# Define AWS region
REGION = "us-east-1"

# Create an STS client to assume roles
sts_client = boto3.client("sts", region_name=REGION)

# Assume the Dev role to get temporary security credentials
assumed_dev_role = sts_client.assume_role(
    RoleArn="arn:aws:iam::941377111974:role/Dev",  
    RoleSessionName="DevSession"
)

# Get temporary credentials from assumed role
creds = assumed_dev_role["Credentials"]

# Initialize S3 client using the temporary credentials
s3_client = boto3.client(
    "s3",
    region_name=REGION,
    aws_access_key_id=creds["AccessKeyId"],
    aws_secret_access_key=creds["SecretAccessKey"],
    aws_session_token=creds["SessionToken"]
)

# Define the S3 bucket name
bucket_name = "fang-demo-bucket"

# Create S3 bucket 
s3_client.create_bucket(
    Bucket=bucket_name
)

print(f"Bucket '{bucket_name}' successfully created.")

# Create and upload text files
with open("assignment1.txt", "w") as f:
    f.write("Empty Assignment 1")
s3_client.upload_file("assignment1.txt", bucket_name, "assignment1.txt")

with open("assignment2.txt", "w") as f:
    f.write("Empty Assignment 2")
s3_client.upload_file("assignment2.txt", bucket_name, "assignment2.txt")

with open("bookimage.jpg", "rb") as file:
    s3_client.put_object(Bucket=bucket_name, Key="bookimage.jpg", Body=file)


print(f"Uploaded files to '{bucket_name}' successfully: assignment1.txt, assignment2.txt, bookimage.jpg.")
