from __future__ import print_function
from Trie import make_trie, in_trie
from datetime import datetime
from calendar import timegm
import regex as re
import boto3
import json
import base64

def lambda_handler(event, context):
	dynamodb = boto3.client("dynamodb")

	checkset = set()

	try:
		with open('games.txt', 'r') as f:
			for line in f:
				checkset.add(line.lower().strip())
			else:
				#no more lines
				f.close()
	except IOError:
		print("Couldn't find games.txt file in Lambda zip file! Terminating..")
		exit()

	trie = make_trie(checkset)
	print('Made trie!')
	try:
		for record in event['Records']:
			#Kinesis data is base64 encoded so decode here
			record=base64.b64decode(record["kinesis"]["data"])
			#print("Decoded payload: " + record)

			jdata = json.loads(record)
			try:

				text = jdata["text"].lower()
				#strip punctuations
				text = re.sub(ur"\p{P}+", "", text)
				answer = in_trie(trie, text)
				if answer[0] == True:
					print("MATCHED: ", answer[1])
					#extract from json 3 things for table. User, MsgID, TS.
					user = jdata["user"]["screen_name"]
					msgid = jdata["id_str"]

					#get epoch time
					created = jdata["created_at"]
					created = created[0:20] + created[26:30]
					#Weekday Month Day HH:MM:SS Year
					date_time = datetime.strptime(created, "%a %b %d %H:%M:%S %Y")
					ts = int(timegm(date_time.timetuple()))

					dynamodb.put_item(TableName="Game", Item={
						"Title": {"S": answer[1]},
						"Time": {"N": str(ts)},
						"User": {"S": user},
						"Msg": {"S": jdata["text"]},
						"MsgID": {"N": msgid},
						}
					)

					print("Insert successful!")
				else:
					print("NO MATCH!")


			except KeyError:
				#deleted status
				continue
	except KeyError:
		print("KeyError where it shouldn't be! Exiting")

