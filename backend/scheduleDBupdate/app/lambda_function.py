import json
import bson
import requests
import urllib
#import boto3
from datetime import datetime
from pymongo import MongoClient
from pymongo.collection import ReturnDocument

# Set Lambda Client to connect with other lambdas internally
#lam = boto3.client('lambda')

# Set Mongo Client
client = MongoClient('mongodb+srv://reviewtrends:Vnso8hRWCI3wg077@cluster0.ujh40.mongodb.net/reviewTrendsDB?retryWrites=true&w=majority')

# Set Database
db = client.reviewTrendsDB
# db = client[os.environ["DB_NAME"]]

def lambda_handler(event, context):
	# set today's date for comparison
	todaysDate = datetime.today()
	
	# Connect to collection
	reviewsAndTrends = db.ReviewsAndTrends
	# reviewsAndTrends = db[os.environ["COLLECTION_NAME"]]

	# Get all property id's and their lastUpdated values
	response_body = reviewsAndTrends.find( {}, { 'propertyId': 1, 'lastUpdated': 1, '_id': 0 } )
	
	# Initiate update for Properties that need to be updated
	# Version 1 - Trigger Lambda
	for document in response_body:
		if 'lastUpdated' in document.keys() and (todaysDate - document["lastUpdated"]).days >= 7:
			# send an asyncronous processing request
			sendProcessingRequest(document["hotelId"], document["lastUpdated"])

	# Version 2 - Put to Queue
#	for document in response_body:
#		if 'lastUpdated' in document.keys() and (todaysDate - document["lastUpdated"]).days >= 7:
			# push to queue
			
			
	return {
		'statusCode': 200
	}

def sendProcessingRequest(hotelId, lastUpdated):
        payload = {}
        payload['hotelId'] = hotelId
        payload['lastUpdated'] = lastUpdated
        print(payload)
        #lam.invoke(FunctionName='updateDB',
        #        InvocationType='Event',
        #        Payload=json.dumps(payload))
        
#def main():
#	print("hello from local machine")
#	lambda_handler({"httpMethod":"GET", "queryStringParameters" : {
#		"token": "yJraWQiOiJ5OTMwTWxtbGRndmY4ZXFZQ2EzWGgrdXpUbE9qMFQ3ZFV2UUV1SDJJbk9FPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoic3R1YnBKejQ1aUItWlZGeFZ6UUh6dyIsInN1YiI6IjdjMDkwNDJiLTJiNDUtNGNjYy1iMTdjLTMyNzEyNGJmZjE2NiIsImNvZ25pdG86Z3JvdXBzIjpbInVzLWVhc3QtMV9pckhXUmxYN2JfR29vZ2xlIl0sImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfaXJIV1JsWDdiIiwiY29nbml0bzp1c2VybmFtZSI6Imdvb2dsZV8xMTA5NTc5Mzc4OTIyOTE1ODMzNzkiLCJub25jZSI6IkpUTXdMeU1EUm51LVRZVW1PVlVueEV4cUEtZWt2XzZKdzRvWHRHdFJNZVlWaWROUGE2YkxGU2xtNGJ0eXJQYnVxY0xlZ21CTzZlYXFtemtqRFMtUlFiOHlRTzc2Wi1TSFdTV2x3YTJuTHduMGs5bHRoaVBhT0thNUU1QUJETFFLdUJFeHZhZkZ6QzFLaGwwTzRnbnI0RmdfNlVORFpWd2E4dWU5ajZZMlcxTSIsImF1ZCI6IjZ0ZWk0YnAzbnVwcHA1bXJlbmIwczQ5NmJxIiwiaWRlbnRpdGllcyI6W3sidXNlcklkIjoiMTEwOTU3OTM3ODkyMjkxNTgzMzc5IiwicHJvdmlkZXJOYW1lIjoiR29vZ2xlIiwicHJvdmlkZXJUeXBlIjoiR29vZ2xlIiwiaXNzdWVyIjpudWxsLCJwcmltYXJ5IjoidHJ1ZSIsImRhdGVDcmVhdGVkIjoiMTYxMzIwOTg1OTIwOCJ9XSwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2MTUyMDY4M#TksIm5hbWUiOiJWZXJvbmlrYSBEbXl0cnlrIiwiZXhwIjoxNjE1MjEwNDE5LCJpYXQiOjE2MTUyMDY4MTksImVtYWlsIjoidmVyb25pa2EuZG15dHJ5a0BnbWFpbC5jb20ifQ.PvRLka4FHmJUQXy7NrP5siJqdkJ3rEUYMvtSU9QayyIef0GOCMxH_VP359LPl8wmvp1Z5wYRpt6u5nt4ygKELByeiEWLB2y07wFH6MvtHHaIWF2GPpM6QCP5KGZt2gQJgKpmC88D0ZyzasQKYADLIUj7vlX4HOPMnAMNJ3LLnGohHFNVRwJJLeElBp8t4eiQiENOdoFsNd30Y_Rff6PXoyCONY_sg0_-SwG-MdOXIto-VxoMkUGQqrbu3bdkCafckvA_QqiQgFt_xkRoqLOFkAaximA3PTEzA6CsLvq58d4WqctTi-hFZOl3eMlY8oBbeLSc2J0zWNDv_pUO8h_XHg",
#		"property_id": "111" }}, None)

#if __name__ == "__main__":
#	main()
