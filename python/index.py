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
        return {
    		'statusCode': 200,
    		'body': response.get('body').get('body'),
    		'headers': {"Access-Control-Allow-Origin": os.environ.get('CORS_DOMAIN', '*')}
    	}
    except Exception as err:
        print(err)
        return {
			'statusCode': 400,
			'body': "error from index file method handler" + str(err),
			'headers': {"Access-Control-Allow-Origin": os.environ.get('CORS_DOMAIN', '*')}
		}

print(handler({ "path": "/hoover-health", "httpMethod": "POST", "body": {"action": "getStatus", "healthcheck_target": "http://127.0.0.1:8000/nfr/security/cvc/sample/" } } , context=None))
