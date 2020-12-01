from packages import urllib3
import json
import os
os.environ['NODE_TLS_REJECT_UNAUTHORIZED'] = '0'

commonHeaders = {

    "Content-Type" : "application/json",
    "Accept" : "application/json",
    "Access-Control-Allow-Origin" : "*",
    "Access-Control-Allow-Origin-Credentials" : "true",
    "Access-Control-Allow-Origin-Methods": "DELETE, POST GET OPTIONS",
    "Access-Control-Allow-Origin-Headers": "Access-Control-Allow-Origin.Content-Type, Access-Control-Allow-Headers, Authorization, X-requested-With, Accet, Access-Control-Allow-Origin-Credentials"
}

commonOptions = {
    "Content-Type" : "application/json",
    "Accept" : "application/json"
}

http = urllib3.PoolManager()

def Get(url, customHeaders, customOptions):
    options={
        **commonOptions,
        **customOptions,
        'url': url,
		'method': "GET",
		'headers': {
			**commonHeaders,
			**customHeaders
		}
    }
    try:
        response = http.request(
            url=options.get('url'),
            method=options.get('method'),
            headers=options.get('headers'),
            timeout=options.get('timeout')
        )
        return response
    except Exception as err:
        return err

# print(Get(url="https://www.google.com", customHeaders=commonHeaders, customOptions=commonOptions))
def Request(url, method, body, customHeaders, customOptions):

    try:
        tempOptions = commonOptions
        for key in tempOptions.keys():
            if customOptions.get(key, 'sample_value') in customOptions:
                del commonOptions[key]

        tempHeaders = customHeaders
        for key in tempHeaders.keys():
            if tempHeaders.get(key, 'sample_value') in customHeaders:
                del commonHeaders[key]

        options={
            **commonOptions,
            **customOptions,
            'url': url,
    		'method': "GET",
    		'headers': {
    			**commonHeaders,
    			**customHeaders
    		}
        }
        if body:
            options['body'] = body

        response = http.request(
            url=options.get('url'),
            method=options.get('method'),
            headers=options.get('headers'),
            timeout=options.get('timeout')
        )

        resBody=""
        if options.get('headers').get('Content-Type') == "application/xml":
            resBody = body
        else:
            resBody = body if (body and isinstance(body, 'object') and body is not None) \
                      else (json.loads(body) if (body and not isinstance(body, 'object') and body is not None) \
                      else "")

            return {
                'body': resBody,
                'status': response.status
            }
    except Exception as err:
        return err
