import boto3
import matplotlib.pyplot as plt
import json
import time
import io

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the current timestamp and calculate the range for the last 10 seconds
    current_event_time = int(time.time())
    ten_seconds_ago = current_event_time - 10
    
    # Query the DynamoDB table
    table = dynamodb.Table('S3-object-size-history')
 
    response = table.query(
        KeyConditionExpression='BucketName = :bucket AND EventTime BETWEEN :start_time AND :end_time',
        ExpressionAttributeValues={
            ':bucket': 'testbucket-for-cloud-assignment2',
            ':start_time': str(ten_seconds_ago),  
            ':end_time': str(current_event_time)
        }
    )
    
    # Prepare data for plotting
    event_times = []
    sizes = []
    for item in response['Items']:
        event_times.append(item['EventTime'])
        sizes.append(item['Size'])
    
    # Sorting the data based on event time
    if event_times:
        event_times, sizes = zip(*sorted(zip(event_times, sizes)))
     

    # Query the DynamoDB table for historical high
    historical_high_response = table.query(
        KeyConditionExpression='BucketName = :bucket AND EventTime = :event_time',
        ExpressionAttributeValues={
            ':bucket': 'testbucket-for-cloud-assignment2',
            ':event_time': 'historical_high'
        }
    )

    # Get the historical high value
    historical_high = 0
    if historical_high_response['Items']:
        historical_high = historical_high_response['Items'][0].get('Size', 0)

    # Plot the data
    plt.figure(figsize=(8, 5))
    plt.plot(event_times, sizes, marker='o', linestyle='-', label='Size Change')
    plt.axhline(y=historical_high, color='r', linestyle='dashed', linewidth=2, label='Historical High')

    plt.xlabel('Event Time (Unix Timestamp)')
    plt.ylabel('Size')
    plt.title('S3 Bucket Size Change Over Last 10 Seconds')
    plt.legend()

    # Save the plot as an image in the bucket
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    
    s3.put_object(Bucket='testbucket-for-cloud-assignment2', Key='plot.png', Body=img_buffer, ContentType='image/png')
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Plot created successfully', 
            'plot_url': 'https://testbucket-for-cloud-assignment2.s3.us-east-1.amazonaws.com/plot.png'})
    }
