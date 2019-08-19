import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('staff')

response = table.scan(
	FilterExpression=Attr('first_name').begins_with('r') &
Attr('account_type').eq('administrator')
)

items = response['Items']
print(items)