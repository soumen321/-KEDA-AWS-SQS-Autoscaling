import boto3
import time
import logging
import os


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Load AWS config from environment (set via Kubernetes Secret)
sqs = boto3.client("sqs", region_name="us-east-1")
queue_url = os.getenv("SQS_QUEUE_URL")

def process_message(msg_body: str):
    """Business logic for processing messages"""
    logging.info(f"Processing message: {msg_body}")
    # TODO: Add your ML pipeline / business logic here
    time.sleep(1)  # simulate work

def main():
    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=5,
            WaitTimeSeconds=10
        )
        messages = response.get("Messages", [])
        if not messages:
            logging.info("No messages, waiting...")
            continue

        for msg in messages:
            process_message(msg["Body"])
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=msg["ReceiptHandle"]
            )
            logging.info("Message deleted")

if __name__ == "__main__":
    main()
