import boto3
import json
import os

def update_campaign_status(campaign_id, user_id, event_timestamp):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.update_item(
        TableName = os.environ['CAMPAIGN_STATUS_TABLE'],
        Key = {
            'campaign_id': {
                'S': campaign_id
            },
            'user_id': {
                'S': user_id
            }
        },
        ExpressionAttributeNames={
            '#err': 'email_response_received'
        },
        ExpressionAttributeValues={
            ':t': {
                'N': str(event_timestamp),
            },
        },
        UpdateExpression='SET #err = :t'
    )

def insert_email_send(campaign_id, user_id, event_timestamp):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.put_item(
        TableName = os.environ['CAMPAIGN_STATUS_TABLE'],
        Item = {
            'campaign_id': {
                'S': campaign_id
            },
            'user_id': {
                'S': user_id
            },
            'email_send': {
                'N': str(event_timestamp)
            },
            'email_response_received': {
                'N': str(0)
            }
        }
    )
    
def lambda_handler(event, context):
    print(event['Records'][0]['body'])
    
    message_body = json.loads(event['Records'][0]['body'])
    event_type = message_body['event_type']
    event_timestamp = message_body['event_timestamp']
    application_id = message_body['application']['app_id']
    campaign_id = message_body['client_context']['custom']['campaign_id']
    user_id = message_body['client_context']['custom']['user_id']
    
    print(event_timestamp)
    print(application_id)
    print(campaign_id)
    print(user_id)
    
    if (event_type == '_email.send'):
        insert_email_send(campaign_id, user_id, event_timestamp)
    elif (event_type == '_email.click'):
        update_campaign_status(campaign_id, user_id, event_timestamp)
    
    # ToDo: improve return type / message
    return 'processing complete.'