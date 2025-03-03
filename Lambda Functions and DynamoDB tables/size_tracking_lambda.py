import boto3
import json
import time

# Connect AWS Resource
dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")

def lambda_handler(event, context):
    current_event_time = str(int(time.time()))  
    bucket_name = "testbucket-for-cloud-assignment2"
    
    print(f"Checking S3 bucket: {bucket_name}...")  
    response = s3.list_objects_v2(Bucket=bucket_name)

    print(f"S3 Response: {response}") 
    
    total_size = 0
    object_count = 0

    # Ensure S3 is not empty
    if "Contents" in response:
        for obj in response["Contents"]:
            total_size += obj["Size"]
            object_count += 1
    print(f"Total objects: {object_count}, Total size: {total_size}")  

    # Connect DynamoDB table
    table = dynamodb.Table("S3-object-size-history")

    # Query `historical_high`
    print("Checking historical high...")
    historical_high = 0
    try:
        response = table.query(
            KeyConditionExpression="BucketName = :bucket AND EventTime = :event_time",
            ExpressionAttributeValues={
                ":bucket": bucket_name,
                ":event_time": "historical_high"
            }
        )
        if "Items" in response and len(response["Items"]) > 0:
            historical_high = response["Items"][0].get("Size", 0)
    except Exception as e:
        print(f"Error fetching historical_high: {str(e)}")  
    
    print(f"Current historical high: {historical_high}")

    # Update if total_size is greater than historical_high
    if total_size > historical_high:
        print(f"Updating historical high to {total_size}...")
        table.put_item(
            Item={
                "BucketName": bucket_name,
                "EventTime": "historical_high",
                "Size": total_size
            }
        )

    # Store current data into DynamoDB
    print(f"Storing current size tracking data at {current_event_time}...")
    table.put_item(
        Item={
            "BucketName": bucket_name,
            "EventTime": current_event_time,
            "Size": total_size,
            "ObjectCount": object_count,
        }
    )

    print("Data successfully written to DynamoDB.")  

    return {
        "statusCode": 200,
        "body": json.dumps(
            f"Size tracking completed. Current size: {total_size}, Object count: {object_count}"
        ),
    }
