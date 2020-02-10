import boto3
import json
import os

def lambda_handler(event, context):
    print(event)
    
    pinpoint = boto3.client('pinpoint')
    response = pinpoint.send_messages(
            ApplicationId=os.environ['APPLICATION_ID'],
            MessageRequest={
                'Context': {
                    'campaign_id': event['campaign_id'],
                    'user_id': event['user_id']
                },
                'Addresses': {
                    event['sms_number']: {
                        'ChannelType': 'SMS'
                    }
                },
                'MessageConfiguration': {
                    'SMSMessage': {
                        'Body': 'Test Message'
                    }
                }
            }
        )
    print(response)
    
    return 'proessing complete.'
