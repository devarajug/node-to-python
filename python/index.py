import json
import route
import os

os.environ['NODE_TLS_REJECT_UNAUTHORIZED'] = '0'

def handler(event, context):
    try:
        routes = route.exports(event.get('path'))
        requestHandler = routes.get(event.get('httpMethod'))
        response = requestHandler(event)

        return {
			'statusCode': 200,
			'body': json.dumps(response),
			'headers': {"Access-Control-Allow-Origin": os.environ.get('CORS_DOMAIN', '*')}
    	}
    except Exception as err:
        print(err)
        return {
			'statusCode': 400,
			'body': err,
			'headers': {"Access-Control-Allow-Origin": os.environ.get('CORS_DOMAIN', '*')}
		}

print(handler({"path":"/hoover-health", "httpMethod":"GET"}, context=None))
