import json
import bson
import requests
import urllib
import boto3
from datetime import datetime
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
from environs import Env

# Useful for hiding env variables which would be understood by github
env = Env()
# read .env file, if it exists
env.read_env()  

# Create Mongo Client
client = MongoClient(env("MONGO_CLIENT_URL_REVIEWS_AND_TRENDS"))

# Create SQS client
sqs = boto3.client('sqs')
queue_url = env("PROPERTIES_TO_PROCESS_QUEUE")

# Access Database
db = client.reviewTrendsDB

def lambda_handler(event, context):
	# Receive message from SQS queue
	print(event["Records"][0])
	propertyId = None
	lastUpdated = None
	if "propertyId" in event["Records"][0]["messageAttributes"]:
		propertyId = event["Records"][0]["messageAttributes"]["propertyId"]["stringValue"]
		
	if "lastUpdated" in event["Records"][0]["messageAttributes"]:
		lastUpdated = event["Records"][0]["messageAttributes"]["lastUpdated"]["stringValue"]
	
	print(propertyId)
	print(lastUpdated)
	
	# Delete received message from queue - if the lambda exited with an error
	# sqs.delete_message(
	#     QueueUrl=queue_url,
	#     ReceiptHandle=receipt_handle
	# )
	
	print('Received and deleted message for propertyID: %s' % propertyId)


	# if "propertyId" in event:
	#     print(event["propertyId"])
	
	# reviews = [];
	# if "lastUpdated" in event:
	#     print(event["lastUpdated"])
		# Just grab the reviews that are newer than the lastUpdated date
		# try{
		#     do{
		#         reviews_chunk = getReviews();
		#         reviews.append(reviews_chunk)
		#     } while (reviews_chunk[99].date < lastUpdated)
		#     trim reviews - delete all reviews from the end that has date < lastUpdated
		# } catch(e){
		#     print(e);
		# }
		
	# else:
		# print("New hotel needs to be processed")
		# If no date is provided, meaning we don't have it in the DB - new hotel to process
		# Just grab the reviews for the last 3 years
		# try{
		#     do{
		#         reviews_chunk = getReviews();
		#         reviews.append(reviews_chunk)
		#     } while (reviews_chunk[99].date < Jan 1, 2019)
		#     trim reviews - delete all reviews from the end that has date < lastUpdated
		# } catch(e){
		#     print(e);
		# }


	# results = callGoogleAPI(reviews)
	# update the DB
		
	return {
		'statusCode': 200,
		'body': json.dumps('Hello from Lambda!')
	}

def main():
	event = {
		"Records":[
			{
				"messageId":"c0bcd616-0495-4abb-861f-ec0e55f3a21e",
				"receiptHandle":"AQEBnIZCCE8qwzzBIn65ncffhjnBBeWAZ/prTqfhOtdjbuNFk7zUov5eq6lpWiKz8HksuvV+BTk9LSNtqq1u25N2ZSw7R2WDNKsdFv44AfEUPAoK0mIQATet/7PrOwgqrklplfA7/piUd60pBMBERLZMms0GJLfxYpkwdjLz++3dEIqtwoKsZ08w+YP01P9iEsBlazz+mJUkrDyy7tAlT4r8eLUeGsjEorJiDKuidnuSAG+lbY4Mn0IWLYbGAtv8k5lzgamcmLY7Ae5RoawL27ddERxvPC4gcqJ+2wkaE89sEjJtv84O1yMHP9ZZeZgnh4UxBt1UEL4uu79FZcjX77nK5qb+WyItC7KmD7YyuzfkoJtgVX0igIF3EjrCHQ662yqISQGWrKgCRflyF9/PDcxNAw==",
				"body":"Hotel with id 58703 needs to be processed",
				"attributes":{
					"ApproximateReceiveCount":"11",
					"SentTimestamp":"1620269982369",
					"SenderId":"AROAZRJG4YTFSS4BFI4YO:user1223250=Veronika_Dmytryk",
					"ApproximateFirstReceiveTimestamp":"1620269982369"
				},
				"messageAttributes":{
					"lastUpdated":{
						"stringValue":"2020-10-11 13:42:25",
						"stringListValues":[],
						"binaryListValues":[],
						"dataType":"String"
					},
					"propertyId":{
						"stringValue":"58703",
						"stringListValues":[],
						"binaryListValues":[],
						"dataType":"Number"
					}
				},
				"md5OfBody":"ab18d901005ca36cfaa2f44dd36960d2",
				"md5OfMessageAttributes":"97c8e197960aedd89c61efbc250022fb",
				"eventSource":"aws:sqs",
				"eventSourceARN":"arn:aws:sqs:us-east-1:655600960715:properties-to-process",
				"awsRegion":"us-east-1"
			}
		]
	}

	lambda_handler(event, None)

if __name__ == "__main__":
	main()