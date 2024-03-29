import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('staff')

table.update_item(
	Key={
		'username': 'ruanb',
		'last_name': 'bekker'
	},
	UpdateExpression='SET age = :vall',
	ExpressionAttributeValues={
		':vall': 29
	}
)