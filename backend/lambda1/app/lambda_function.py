import jwt
import bson
import json
import trio

async def lambda_handler(event, context):
	# Print received event
	print("Received event: " + json.dumps(event, indent=2))
	
	if ("httpMethod" in event) and (event["httpMethod"] == "GET") and ("token" in event["queryStringParameters"]):
		print("getting the token")
		token = event["queryStringParameters"]["token"]
		# algorithm that was used to encode and client_id of our app in Cognito
		algorithm = ["RS256"]

		# client id of our app in Cognito
		aud = "6tei4bp3nuppp5mrenb0s496bq"
		try:
			# Decode the token
			payload = decodeToken(token, algorithm, aud)
			print("Success")
			return {
			    'statusCode': 200,
			    'body': json.dumps(payload, default=json_unknown_type_handler)
			}
		except Exception as e:
			print("Exception: ", e)
			response_body = {
				"error": str(e)
			}
			return {
			    "statusCode": 403,
			    "body": json.dumps(response_body)
			}
		
	else:
		print("Wrong method or no token")
		return {
		    'statusCode': 400,
		    'body': json.dumps({"error": "Use GET method and pass token"})
		}
        
    

def decodeToken(token, algorithm, aud):
	#  open the file with public key
	with open('./public_key.json') as f:
		jwks = json.load(f)
		
	# retrieve all public keys
	public_keys = {}
	for jwk in jwks['keys']:
		kid = jwk['kid']
		public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

	# get the correct public key for this token 
	# kid field should match between token and the key
	kid = jwt.get_unverified_header(token)['kid']
	key = public_keys[kid]

	print("decoding the token...")
	try:
		result = jwt.decode(
		    token,
		    key=key,
		    audience = aud,
		    algorithms=algorithm,
		    verify_exp=True
		)
	except Exception as e:
		raise e

	return result

# JSON cannot serialize decimal, datetime and ObjectId. So we provide this handler.
def json_unknown_type_handler(x):
    if isinstance(x, bson.ObjectId):
        return str(x)
    raise TypeError("Unknown datetime type")


