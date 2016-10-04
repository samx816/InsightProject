import boto3
import botocore

dynamodb = boto3.resource('dynamodb')
try:
	table = dynamodb.create_table(TableName='Game', KeySchema=[
		{
			'AttributeName': 'Title',
			'KeyType': 'HASH' #Partition key
		},
		{
			'AttributeName': 'TimeEnoch',
			'KeyType': 'RANGE' #Sort key
		}
		],
		AttributeDefinitions=[
		{
			'AttributeName': 'Title',
			'AttributeType': 'S'
		},
		{
			'AttributeName': 'TimeEnoch',
			'AttributeType': 'N'
		}
		],
		ProvisionedThroughput={
			'ReadCapacityUnits': 5,
			'WriteCapacityUnits': 5
		}
		)
except botocore.exceptions.ClientError:
	print('Game exists!')
