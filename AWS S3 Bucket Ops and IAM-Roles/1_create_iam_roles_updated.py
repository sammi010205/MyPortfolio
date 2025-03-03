import boto3
import json

# Set up IAM client
iam = boto3.client("iam")

# Trust policy definition for role assumption
assume_role_trust_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": "*"},
            "Action": "sts:AssumeRole"
        }
    ]
}

# Create Dev Role with full S3 access
dev_role = iam.create_role(
    RoleName="Dev",
    AssumeRolePolicyDocument=json.dumps(assume_role_trust_policy)
)
iam.attach_role_policy(
    RoleName="Dev",
    PolicyArn="arn:aws:iam::aws:policy/AmazonS3FullAccess"
)

# Create User Role with specific S3 permissions
user_role = iam.create_role(
    RoleName="User",
    AssumeRolePolicyDocument=json.dumps(assume_role_trust_policy)
)

# Define a custom policy allowing listing S3 buckets/objects
user_access_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["s3:ListBucket", "s3:GetObject"],
            "Resource": ["arn:aws:s3:::*"]
        }
    ]
}

iam.put_role_policy(
    RoleName="User",
    PolicyName="LimitedS3Access",
    PolicyDocument=json.dumps(user_access_policy)
)

print(" 'Dev' and 'User' roles successfully created.") 


