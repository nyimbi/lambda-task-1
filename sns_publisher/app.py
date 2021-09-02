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
    logger.info("created queue")
    logger.info("Event: %s", event)
    # What sort of event do we have API or SQS (Does it Matter)

    # Extract values from the Event

    # Only available if the event is an APi call
    http_method = event.get("httpMethod")
    body = event.get("body")
    print(body)

    if http_method is not None:
        prod_id = json.loads(body).get("productID")
        txt_flds = json.loads(body).get("textFields")
    else:
        prod_id = event["productID"]
        txt_flds = event["textFields"]

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

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": msg,
            }
        ),
    }
