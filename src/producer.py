import boto3
import os

sqs = boto3.client("sqs", region_name="us-east-1")
queue_url =  os.getenv("SQS_QUEUE_URL")

def send_message(msg: str):
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=msg
    )
    print(f"Message sent: {response['MessageId']}")

if __name__ == "__main__":
    for i in range(30):
        send_message(f"Test Hello Message KEDA {i}")
