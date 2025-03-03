import boto3
import time

s3 = boto3.client('s3')
lambda_client = boto3.client('lambda')
bucket_name = 'testbucket-for-cloud-assignment2'

def lambda_handler(event, context):
    # Create object
    s3.put_object(Bucket=bucket_name, Key='assignment1.txt', Body='Empty Assignment 1')
    time.sleep(2)
    
    # Update object
    s3.put_object(Bucket=bucket_name, Key='assignment1.txt', Body='Empty Assignment 2222222222')
    time.sleep(2)
    
    # Delete object
    s3.delete_object(Bucket=bucket_name, Key='assignment1.txt')
    time.sleep(2)
    
    # Create another object
    s3.put_object(Bucket=bucket_name, Key='assignment2.txt', Body='33')
    
    # Call Plotting Lambda API
    print("Invoking plotting_lambda...")
    response = lambda_client.invoke(
            FunctionName="plotting_lambda",
            InvocationType="RequestResponse"
    )
    
    return {
        'statusCode': 200,
        'body': 'Driver Lambda executed successfully'
    }
