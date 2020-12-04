import os
import ast
import json
import route


os.environ['NODE_TLS_REJECT_UNAUTHORIZED'] = '0'

def handler(event, context=None):
    try:
        temp = json.dumps(ast.literal_eval(str(event)))
        event = json.loads(temp)
        routes = route.exports(event.get('path'))
        if not isinstance(routes, dict):
            raise Exception("Invalid Path")
        requestHandler = routes.get(event.get('httpMethod'))
        response = requestHandler(event)
        result = {
    		'statusCode': response.get('status'),
    		'body': response.get('body') if isinstance(response, dict) and response.get('body', None) else str(response),
    		'headers': {"Access-Control-Allow-Origin": os.environ.get('CORS_DOMAIN', '*')}
    	}
    except Exception as err:
        print(err)
        result = {
			'statusCode': 400,
			'body': "error from index file method handler" + str(err),
			'headers': {"Access-Control-Allow-Origin": os.environ.get('CORS_DOMAIN', '*')}
		}
    return result

print(handler({ "path": "/hoover-health", "httpMethod": "GET", "body": {"action": "getStatus", "healthcheck_target": "http://127.0.0.1:8000/nfr/security/cvc/sample/" } } , context=None))
