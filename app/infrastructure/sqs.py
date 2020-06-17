import boto3
from dynaconf import settings


class SqsClient:
    def __init__(self, queue_url):
        self.client = boto3.client('sqs', region_name=settings.SQS.REGION)
        self.queue_url = queue_url
        self.messages_per_polling = settings.SQS.MESSAGES_PER_POLLING
        self.visibility_timeout = settings.SQS.VISIBILITY_TIMEOUT
        self.wait_time = settings.SQS.WAIT_TIME

    def send_message(self, message):
        self.client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=message
        )

    def read_messages(self):
        response = self.client.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=self.messages_per_polling,
            VisibilityTimeout=self.visibility_timeout,
            WaitTimeSeconds=self.wait_time
        )

        messages = []
        if response.get('Messages'):
            messages = map(lambda msg: msg, response.get('Messages'))

        return messages

    def delete_message(self, message):
        self.client.delete_message(
            QueueUrl=self.queue_url,
            ReceiptHandle=message.get('ReceiptHandle')
        )

    def get_message_body(self, message):
        return message.get('Body')
