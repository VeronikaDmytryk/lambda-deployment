from lambda_function import lambda_handler

async def allJobsAreScheduled():
    response = lambda_handler({"httpMethod":"GET", "queryStringParameters" : {}}, None)
    assert response['statusCode'] == 200