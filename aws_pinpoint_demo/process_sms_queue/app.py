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
            '#ssnt': 'sms_send'
        },
        ExpressionAttributeValues={
            ':t': {
                'N': str(event_timestamp),
            },
        },
        UpdateExpression='SET #ssnt = :t'
    )
    
def lambda_handler(event, context):
    print(event['Records'][0]['body'])
    
    message_body = json.loads(event['Records'][0]['body'])
    event_type = message_body['event_type']
    event_timestamp = message_body['event_timestamp']
    application_id = message_body['application']['app_id']
    campaign_id = json.loads(message_body['attributes']['customer_context'])['campaign_id']
    user_id = json.loads(message_body['attributes']['customer_context'])['user_id']
    
    if (event_type == '_SMS.SUCCESS'):
        update_campaign_status(campaign_id, user_id, event_timestamp)
    
    # ToDo: improve return type / message
    return 'processing complete.'