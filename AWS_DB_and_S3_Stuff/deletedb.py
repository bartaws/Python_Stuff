import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('staff')

table.delete_item(
	Key={
		'username': 'ruanb',
		'last_name': 'bekker'
	}
)