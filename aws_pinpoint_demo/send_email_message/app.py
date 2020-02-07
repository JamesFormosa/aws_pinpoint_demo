import boto3
import json

def lambda_handler(event, context):
    print(event)
    s3 = boto3.client('s3')
    s3.download_file('change-pinpoint-templates', event['message_template'], '/tmp/pinpoint_template.html')
    with open ("/tmp/pinpoint_template.html", "r") as myfile:
        data=myfile.readlines()
    print(data[0])
    pinpoint = boto3.client('pinpoint')
    response = pinpoint.send_messages(
            ApplicationId='c83228417e1e4619a61fabcfaef18b1a',
            MessageRequest={
                'Context': {
                    'campaign_id': event['campaign_id'],
                    'user_id': event['user_id']
                },
                'Addresses': {
                    'formosa@amazon.com': {
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

