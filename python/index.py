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
    except:
        print(sys.exc_info()[1])
        return {
			'statusCode': 400,
			'body': sys.exc_info(),
			'headers': {"Access-Control-Allow-Origin": }#process.env.CORS_DOMAIN} need to set
		}
