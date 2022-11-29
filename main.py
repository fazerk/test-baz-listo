import requests
import json
import logging

from aws.sqs import SQS

logging.basicConfig(level=logging.INFO)


def get_data():
    url = "https://jsonplaceholder.typicode.com/posts"
    data = requests.get(url=url)
    data_json = data.json()
    keys = set([key['userId'] for key in data_json])
    result = []
    for key in keys:
        filter_data = list(filter(lambda x: x['userId'] == key, data_json))
        json_object = {key: {"records": filter_data}}
        result.append(json_object)

    message = json.dumps(result)
    logging.info(f'{message}')

    # Publish to Queue the transformed data
    sqs = SQS(sqs_name="redsocial-ws-tasks-test")
    if sqs.queue:
        response = sqs.send_message(message=message)
        if response:
            logging.info(f'{response}')
        else:
            logging.error("Error sending message")

        # Pull data from the queue
        messages = sqs.get_messages()
        logging.info(f'{messages}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_data()
