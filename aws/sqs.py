import boto3
import logging

sqs_resource = boto3.resource('sqs')
logging.basicConfig(level=logging.INFO)


class SQS:
    def __init__(self, sqs_name: str):
        try:
            self.queue = sqs_resource.get_queue_by_name(QueueName=sqs_name)
        except Exception as e:
            self.queue = None
            logging.error(f"{e}")

    def send_message(self, message: str):
        try:
            response = self.queue.send_message(MessageBody=message)
            return response
        except Exception as e:
            logging.error(f"{e}")
            return None

    def get_messages(self):
        response = self.queue.receive_messages()
        return response
