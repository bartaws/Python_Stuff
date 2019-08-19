import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('staff')

with table.batch_writer() as batch:
	batch.put_item(
		Item={
			'account_type': 'standard_user',
			'username': 'stefanb',
			'first_name': 'stefan',
			'last_name': 'bester',
			'age': 30,
			'address': {
				'road': '1 jamesville street',
				'city': 'kroonstad',
				'province': 'free state',
				'country': 'south africa'

			}
		}
	)
	batch.put_item(
		Item={
			'account_type': 'administrator',
			'username': 'ruanb',
			'first_name': 'ruan',
			'last_name': 'bekker',
			'age': 30,
			'address': {
				'road': '10 peterville street',
				'city': 'cape town',
				'province': 'western cape',
				'country': 'south africa'
			}
		}
	)
	batch.put_item(
		Item={
			'account_type': 'standard_user',
			'username': 'samanthas',
			'first_name': 'samantha',
			'last_name': 'smith',
			'age': 28,
			'address': {
				'road': '12 newton street',
				'city': 'port elizabeth',
				'province': 'eastern cape',
				'country': 'south africa'
			}
		}
	)