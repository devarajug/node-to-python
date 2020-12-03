import json
from healthCheck import (
    atlassianEndpoints,
    getStatus
)

def healthHandler(event):
    try:
        if event.get('httpMethod') == 'GET':
            return atlassianEndpoints()
        elif event.get('httpMethod') == 'POST':
            data = event.get('body')
            if data.get("action") == "getStatus":
                return getStatus(data)
            else:
                raise Exception("Invalid Method")
        else:
            raise Exception("Invalid Method")

    except Exception as e:
        return "error from healthHandler method from handler file" + str(e)
