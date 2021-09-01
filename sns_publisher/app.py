import json
import boto3
import logging
import os

# setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# import requests
FLAGGED_WORDS = ['oracle', 'microsoft', 'google', 'symantech', 'siemens', 'aws']

INQUEUE = os.environ.get('INQUEUE')
MAXMSG = int(os.environ.get('MAXMSG'))
SNSTOPIC = os.environ.get('SNSTOPIC')


def lambda_handler(event, context):
    found = False
    ret_word =[]
    # create  sqs service resource
    sqs = boto3.resource('sqs')
    # get queue
    queue = sqs.Queue(INQUEUE)
    logger.info('created queue')
    logger.info('Event: %s', event)

    # Extract values from the Event
    prod_id = event['productID']
    txt_flds = event['textFields']

    # Convert the json to a string
    #suboptimal we search both keys and values
    s = json.dumps(txt_flds).lower()
    logger.info('textFields: %s', s)

    # Scan for flagged words in the textFields string
    for word in FLAGGED_WORDS:
        if word in s:
            found = True
            ret_word.append(word)

    # Get the SNS resource
    sns = boto3.resource('sns')
    # Get the queue
    topic = sns.Topic(SNSTOPIC)
    if found:
        logger.info(json.dumps({
            "productID": prod_id,
            "textFields": txt_flds,
            "found": str(found)
        }))
        msg = json.dumps({
                "productID": prod_id,
                "flaggedWords": '[' +','.join(ret_word)+']',
            })

        print(msg)
        # TODO Change this once we know it works
        response = topic.publish(
            Subject="Flagged Words Found",
            Message=msg
        )
    # else:
    #     pass # Leaving this here because we don't have to send anything if not found

