import tweepy
from tweepy import OAuthHandler
from tweepy import StreamListener
from tweepy import Stream
from requests.packages.urllib3.exceptions import ProtocolError

import sys
import json
import time

import boto3

#for twitter stream
class Listen(StreamListener):
	count = 1
	shardCt = 4
	def on_data(self, data):
		kinesis.put_record(StreamName=kstream, Data=data, PartitionKey=str(Listen.count))
		Listen.count = (Listen.count+1) % Listen.shardCt
		return True

	def on_error(self, status):
		print(status)

if len(sys.argv) <  2:
	print("Not enough arguments! Please specify file to find access keys to Twitter API")
	print("File format: 4 lines, one code on each line")
	print("Consumer key \nConsumer secret \nAccess token \nAccess secret")
	exit()

file = sys.argv[1]

try:
	f = open(file, 'r')

except FileNotFound:
	print "File not found! Terminating"
	exit()

key1 = f.readline().strip()
key2 = f.readline().strip()
key3 = f.readline().strip()
key4 = f.readline().strip()

#setting up twitter stream with proper authorizations
auth = OAuthHandler(key1, key2)
auth.set_access_token(key3, key4)
stream = Stream(auth, Listen())

kinesis = boto3.client("kinesis")
kstream = 'snstream'

if kstream not in [f for f in kinesis.list_streams()['StreamNames']]:
	print 'Creating Kinesis stream %s' % kstream
	kinesis.create_stream(StreamName = kstream, ShardCount = Listen.shardCt)
else:
	print 'Kinesis stream already exists'

while kinesis.describe_stream(StreamName=kstream)['StreamDescription']['StreamStatus'] == 'CREATING':
	time.sleep(2)

print("Streaming now..")
while True:
	try:
		t = stream.sample()
	except KeyboardInterrupt:
		print 'Stopping..'
		opt = raw_input("delete stream? (y/n) ")
		if opt == 'y':
			print("Deleting..")
			kinesis.delete_stream(StreamName=kstream)
		exit()
	except ProtocolError:
		print 'Incomplete read crashed the stream! Restarting Twitter stream..'
		continue
	except AttributeError:
		#stream returned NoneType, or no tweet
		continue
