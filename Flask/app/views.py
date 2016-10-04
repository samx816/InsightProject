from app import app
from flask import render_template, request
import boto3
from boto3.dynamodb.conditions import Key, Attr
import os
from calendar import timegm
from datetime import datetime
file = open('access/access.txt', 'r')

key1 = file.readline().strip()
key2 = file.readline().strip()
os.environ['AWS_ACCESS_KEY_ID'] = key1
os.environ['AWS_SECRET_ACCESS_KEY'] = key2

dynamo = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamo.Table('Game')

def queryGame(game, time1, time2):
	game = game.lower()
	t1 = datetime.strptime(time1, "%m/%d/%Y %H:%M:%S")
	t1 = int(timegm(t1.timetuple()))
	t2 = datetime.strptime(time2, "%m/%d/%Y %H:%M:%S")
	t2 = int(timegm(t2.timetuple()))
	results = table.query(KeyConditionExpression=Key('Title').eq(game) & 
		Key('TimeEnoch').between(t1, t2))
	return results

@app.route('/query')
def query():
	return render_template("query.html")

@app.route("/query", methods=['POST'])
def query_post():
	game = request.form['gameid']
	time1 = request.form['start']
	time2 = request.form['end']
	results = queryGame(game, time1, time2)
	jsonform = [{"User": x["User"], "Time": datetime.fromtimestamp(x["TimeEnoch"]).strftime("%c"), "Message": x["Msg"]} for x in results["Items"]]
	return render_template("queryop.html", output=jsonform, gameid = game, start = time1, end = time2, count = results['Count'])

@app.route('/')
@app.route('/index')
def index():
	return render_template("base.html")

