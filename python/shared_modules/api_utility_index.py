import os
import json
import urllib3

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
        return "error in api utility index from Get method" + str(err)

# print(Get(url="http://127.0.0.1:8000/nfr/security/cvc/sample/", customHeaders=commonHeaders, customOptions=commonOptions))
def Request(url, method, body=None, customHeaders=None, customOptions=None):

    try:
        options={
            **commonOptions,
            'url': url,
    		'method': method,
    		'headers': {
    			**commonHeaders,
    		}
        }

        if customHeaders:
            if customHeaders.get('Authorization', None):
                usename = customHeaders.get('Authorization').get('usename')
                password = customHeaders.get('Authorization').get('password')
                authentication_header = urllib3.make_headers(basic_auth=username+':'+password)
                del customHeaders['Authorization']
                customHeaders.update(authentication_header)

                tempHeaders = customHeaders
                for key in tempHeaders.keys():
                    if tempHeaders.get(key, 'sample_value') in commonHeaders:
                        del commonHeaders[key]
                options.get('headers').update(customHeaders)

        if customOptions:
            tempOptions = commonOptions
            for key in tempOptions.keys():
                if customOptions.get(key, 'sample_value') in commonOptions:
                    del commonOptions[key]

            options.update(customOptions)


        if body:
            options['body'] = body

        if options.get('timeout'):
            timeout = options.get('timeout')
            del options['timeout']
            response = http.request(
                url=options.get('url'),
                method=options.get('method'),
                headers=options.get('headers'),
                timeout=timeout
            )
        else:
            response = http.request(
                url=options.get('url'),
                method=options.get('method'),
                headers=options.get('headers'),
            )
        body = response.data
        resBody=""
        if options.get('headers').get('Content-Type') == "application/xml":
            resBody = body
        else:
            resBody = body if (body and isinstance(body, bytes) and body is not None) \
                      else (json.loads(body) if (body and not isinstance(body, bytes) and body is not None) \
                      else "")

            result = {
                'body': resBody if resBody else "",
                'status': response.status
            }

    except Exception as err:
        result = {
            'status':404,
            'body' :"error in api utility index from Request method" + str(err),
        }

    return result
