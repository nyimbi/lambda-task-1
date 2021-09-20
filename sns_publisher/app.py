import json
import boto3
import logging
import os

# setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# import requests
FLAGGED_WORDS = ["oracle", "microsoft", "google", "symantech", "siemens", "aws"]

INQUEUE = os.environ.get("INQUEUE")
MAXMSG = int(os.environ.get("MAXMSG"))
SNSTOPIC = os.environ.get("SNSTOPIC")


def lambda_handler(event, context):
    found = False
    ret_word = []
    msg = ""
    # create  sqs service resource
    sqs = boto3.resource("sqs")
    # get queue
    queue = sqs.Queue(INQUEUE)
    # What sort of event do we have API or SQS (Does it Matter)
    # Extract values from the Event
    for record in event["Records"]:
        payl = record["body"]
        payload = json.loads(payl)
        prod_id = payload["productID"]
        txt_flds = payload["textFields"]
        print("textFields:", txt_flds)

        # Convert the json to a string
        # suboptimal we search both keys and values
        s = json.dumps(txt_flds).lower()
        logger.info("textFields: %s", s)

        # Scan for flagged words in the textFields string
        for word in FLAGGED_WORDS:
            if word in s:
                found = True
                ret_word.append(word)

        # Get the SNS resource
        sns = boto3.resource("sns")
        sns_client = boto3.client('sns')
        # Get the queue
        topic = sns.Topic(SNSTOPIC)
        if found:
            logger.info(
                json.dumps(
                    {"productID": prod_id, "textFields": txt_flds, "found": str(found)}
                )
            )
            msg = json.dumps(
                {
                    "productID": prod_id,
                    "flaggedWords": "[" + ",".join(ret_word) + "]",
                }
            )

            print(msg)
        if msg == "":
            msg = "Nothing Found"

        sns_response = sns_client.publish(
            TopicArn=topic.arn,
            Message=json.dumps({"default": json.dumps(msg)}),
            MessageStructure="json",
        )

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": msg,
                }
            ),
        }
