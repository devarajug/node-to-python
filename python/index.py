import json
import route
import sys
# process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = 0; idhi tarawath set cheyyali

def handler(event, context):
    try:
        routes = route(event.get('path'))
        # roues = {'post':handler, 'get': handler}
        requestHandler = routes.get(event.get('httpMethod'))
        response = requestHandler(event)
        return {
			'statusCode': 200,
			'body': json.dumps(response),
			'headers': {"Access-Control-Allow-Origin": }#process.env.CORS_DOMAIN} need to set
    	}
    except Exception as err:
        print(err)
        return {
			'statusCode': 400,
			'body': err,
			'headers': {"Access-Control-Allow-Origin": }#process.env.CORS_DOMAIN} need to set
		}
