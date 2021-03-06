# AWS Lambda Badge - Task 1 - Queue Processor

This project contains source code and supporting files for a deployed serverless application that can be deployed with the SAM CLI. 
It includes the following files and folders.

- sns_publisher - Code for the application's Lambda function in python
- events - Sample Invocation events that you can use to test Lambda the function.
- tests - Unit tests for the application code. 
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including 
- A Lambda functions
- An SNS Topic
- An SQS Queue
 
## Testing the deployed application
You can test the application as follows:
On the AWS Console go to:
Go to Amazon SQS > Queues > NyimbiINQueue > Send and receive messages
Copy and paste this message:
```bash
{
  "productID": "xyzzy420",
  "textFields": {
    "title": "How to use Oracle Cloud",
    "description": "The definitive guide to using the world's leading cloud platform that isn't AWS, Azure, GCP, or several others."
  }
}
```
and "Send Message"
If you are subscribed to the SNS topic NyimbiSNSTopic, you will get an email with the result:
```bash
{"message": "{\"productID\": \"xyzzy420\", \"flaggedWords\": \"[oracle,aws]\"}"}
```

## How to Deploy the application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy the application for the first time, run the following in your shell:

```bash
sam build
sam deploy --guided
```

