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
			'body': json.dumps(ast.literal_eval(str(response))),
			'headers': {"Access-Control-Allow-Origin": os.environ.get('CORS_DOMAIN', '*')}
    	}
    except Exception as err:
        # print(err)
        return {
			'statusCode': 400,
			'body': str(err),
			'headers': {"Access-Control-Allow-Origin": os.environ.get('CORS_DOMAIN', '*')}
		}

print(handler({"path":"/hoover-healths", "httpMethod":"GET"}, context=None))
