import json
from healthCheck import (
    atlassianEndpoints,
    getStatus
)

def healthHandler(event):
    try:
        if event.get('httpMethod') == 'GET':
            result = atlassianEndpoints()
        elif event.get('httpMethod') == 'POST':
            data = event.get('body')
            if data.get("action") == "getStatus":
                result = getStatus(data)
            else:
                raise Exception("Invalid Method")
        else:
            raise Exception("Invalid Method")

    except Exception as e:
        result = {
            'statusCode' : 400,
            'message' : "error from healthHandler method from handler file" + str(e)
        }

    return result
