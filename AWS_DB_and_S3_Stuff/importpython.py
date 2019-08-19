import boto3

dynamodb = boto3.resource("dynamodb")

table = dynamodb.create_table(
	TableName = "staff",
	KeySchema=[
		{
			"AttributeName": "username",
			"KeyType": "HASH"
		},
		{
			"AttributeName": "last_name",
			"KeyType": "RANGE"
		}
	],
	AttributeDefinitions=[
		{
			"AttributeName": "username",
			"AttributeName": "S"
		},
		{
			"AttributeName": "last_name",
			"AttributeType": "S"
		},
	],
	ProvisionedThroughput={
		"ReadCapacityUnits": 1,
		"WriteCapacityUnits": 1
	}
)

table.meta.client.get_waiter("table_exists").wait(TableName="staff")
print(table.item_count)