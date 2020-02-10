import base64
import boto3
import json
import os

def lambda_handler(event, context):
    payload=base64.b64decode(event['Records'][0]["kinesis"]["data"])
    
    sqs = boto3.client('sqs')
    print("Decoded payload: " + str(payload))
    msg = json.loads(payload)
    event_type = msg['event_type']
    #print('event_type: ' + msg['event_type'])
    #print('campaign_id: ' + msg['attributes']['campaign_id'])
    
    if (event_type[:6] == '_email'):
        #print('message_id: ' + msg['facets']['email_channel']['mail_event']['mail']['message_id'])
        response = sqs.send_message(
            QueueUrl = os.environ['EMAIL_QUEUE'],
            MessageBody = json.dumps(msg)
        )
    elif (event_type[:4] == '_SMS'):
        #print('message_id: ' + msg['attributes']['message_id'])
        response = sqs.send_message(
            QueueUrl = os.environ['SMS_QUEUE'],
            MessageBody = json.dumps(msg)
        )
    else:   
        response = sqs.send_message(
            QueueUrl = os.environ['CATCH_ALL_QUEUE'],
            MessageBody = json.dumps(msg)
        )
    # ToDo: improve return type / message
    return 'processing complete.'