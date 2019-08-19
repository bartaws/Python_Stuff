import boto3


def create_table(**kwargs):
    """
    This creates a new table in Dynamo
    args: table_name, region_name, partition_key, sort_key, throughput, indexes, attributedefs
    """
    table_name = kwargs['table_name']
    region_name = kwargs['region_name']
    profile = kwargs['profile']
    partition_key = kwargs['partition_key']
    if 'sort_key' in kwargs.keys():
        sort_key = kwargs['sort_key']
    else:
        sort_key = ''
    if 'throughput' in kwargs.keys():
        throughput = kwargs['throughput']
    else:
        throughput = '5'
    if 'indexes' in kwargs.keys():
        indexes = kwargs['indexes']
    else:
        indexes = ''
    if 'attributedefs' in kwargs.keys():
        attributedefs = kwargs['attributedefs']
    else:
        attributedefs = ''

    print ("creating necessary table...")
    session = boto3.session.Session(profile_name=profile)
    dynamodb = session.resource('dynamodb', region_name=region_name)

    throughput = int(throughput)
    if indexes:
        for index in indexes:
            index['ProvisionedThroughput']['ReadCapacityUnits'] = int(index['ProvisionedThroughput']['ReadCapacityUnits'])
            index['ProvisionedThroughput']['WriteCapacityUnits'] = int(index['ProvisionedThroughput']['WriteCapacityUnits'])

    if not sort_key and not indexes:
        new_table = dynamodb.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName' : partition_key,
                    'AttributeType' : 'S',
                },
            ],
            KeySchema=[
                {
                    'AttributeName' : partition_key,
                    'KeyType' : 'HASH',
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': throughput,
                'WriteCapacityUnits': throughput,
            },
            TableName=table_name,
        )
    elif not indexes and sort_key:
        new_table = dynamodb.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName' : partition_key,
                    'AttributeType' : 'S',
                },
                {
                    'AttributeName' : sort_key,
                    'AttributeType' : 'S',
                }
            ],
            KeySchema=[
                {
                    'AttributeName' : partition_key,
                    'KeyType' : 'HASH',
                },
                {
                    'AttributeName' : sort_key,
                    'KeyType' : 'RANGE',
                }
             ],
            ProvisionedThroughput={
                'ReadCapacityUnits': throughput,
                'WriteCapacityUnits': throughput,
            },
            TableName=table_name,
        )
    elif not sort_key and indexes:
        if partition_key == 'Master_UUID': # master table
            attributedefs.append(
                {
                    "AttributeName" : 'Master_UUID',
                    "AttributeType" : "S"
                }
            )
        try:
            new_table = dynamodb.create_table(
                AttributeDefinitions=attributedefs,
                KeySchema=[
                    {
                        'AttributeName' : partition_key,
                        'KeyType' : 'HASH',
                    },
                ],
                GlobalSecondaryIndexes=indexes,
                ProvisionedThroughput={
                    'ReadCapacityUnits': throughput,
                    'WriteCapacityUnits': throughput,
                },
                TableName=table_name,
            )
        except:
            error = sys.exc_info()
            print ('Dynamo Create Table Error:', error)
    else: #index and sort_key
        if partition_key == 'Master_UUID': # master table
            attributedefs.append(
                {
                    "AttributeName" : 'Master_UUID',
                    "AttributeType" : "S"
                }
            )
            attributedefs.append(
                {
                    'AttributeName' : sort_key,
                    'AttributeType' : 'S',
                }
            )
        else:
            attributedefs.append(
                {
                    'AttributeName' : sort_key,
                    'AttributeType' : 'S',
                }
            )
        try:
            new_table = dynamodb.create_table(
                AttributeDefinitions=attributedefs,
                KeySchema=[
                    {
                        'AttributeName' : partition_key,
                        'KeyType' : 'HASH',
                    },
                    {
                        'AttributeName' : sort_key,
                        'KeyType' : 'RANGE',
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': throughput,
                    'WriteCapacityUnits': throughput,
                },
                TableName=table_name,
                GlobalSecondaryIndexes=indexes,
            )
        except:
            error = sys.exc_info()
            print ('Dynamo Create Table Error:', error)

    print ("Waiting for table creation...")
    new_table.wait_until_exists()
    print ("Table Created!")  
    return


print(boto3.session.Session().available_profiles)



myTable = {
    "table_name": "minuntaulu",
    "region_name": "eu-central-1",
    "partition_key": "nimi",
    "sort_key": "sukunimi",
    "profile": "default"
}

dynamodb = boto3.resource('dynamodb')

dynamodb.Table('minuntaulu').put_item(
   Item={
        'nimi': 'bardhyl',
        'sukunimi': 'shatri',
        'last_name': 'asd',
        'age': 253,
         'account_type': 'standard_user',
    }
)

def putFiveItems():
    for i in range(5):
        dynamodb.Table('minuntaulu').put_item(
            Item={
            'nimi': 'user' + str(i),
            'sukunimi': 'academy' + str(i),
            'last_name': 'asd',
            'age': i,
})   

putFiveItems()
    
with table.batch_writer() as batch:
    for i in range(50):
        batch.put_item(
            Item={
                'account_type': 'anonymous',
                'username': 'user' + str(i),
                'first_name': 'unknown',
                'last_name': 'unknown'
            }
        )

#create_table(**myTable)