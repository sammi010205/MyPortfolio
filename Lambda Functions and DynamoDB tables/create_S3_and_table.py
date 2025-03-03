import boto3

# Create an S3 Client
s3_client = boto3.client('s3')
# Create a DynamoDB client
dynamodb_client = boto3.client('dynamodb')

# Create S3 bucket
bucket_name = 'testbucket-for-cloud-assignment2'
s3_client.create_bucket(Bucket=bucket_name)

# Create DynamoDB table，for tracking object sizes
table_name = 'S3-object-size-history'
dynamodb_client.create_table(
    TableName=table_name,
    KeySchema=[
        {
            'AttributeName': 'BucketName',  # Partition key
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'EventTime',  # Sort key
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {'AttributeName': 'BucketName', 'AttributeType': 'S'},
        {'AttributeName': 'EventTime', 'AttributeType': 'S'},
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

print(f"S3 bucket and DynamoDB table '{table_name}' created successfully.")
