import boto3
import json
import os

def lambda_handler(event, context):
    print(event)
    s3 = boto3.client('s3')
    s3.download_file(os.environ['TEMPLATE_BUCKET'], event['message_template'], '/tmp/pinpoint_template.html')
    with open ("/tmp/pinpoint_template.html", "r") as myfile:
        data=myfile.readlines()
    print(data[0])
    pinpoint = boto3.client('pinpoint')
    response = pinpoint.send_messages(
            ApplicationId=os.environ['APPLICATION_ID'],
            MessageRequest={
                'Context': {
                    'campaign_id': event['campaign_id'],
                    'user_id': event['user_id']
                },
                'Addresses': {
                        event['email_address']: {
                        'ChannelType': 'EMAIL'
                    }
                },
                'MessageConfiguration': {
                    'EmailMessage': {
                        'SimpleEmail': {
                            'Subject': {
                                'Data': 'Pinpoint Testing'
                            },
                            'HtmlPart':{
                                'Data': data[0]
                            }
                        }
                    }
                }
            }
        )
    print(response)

