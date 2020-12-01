import json
from healthCheck import (
    atlassianEndpoints,
    getAppNames,
    reportIncident,
    getCustomEndpoints,
    addApp,
    getStatus
)

def healthHandler(event):
    try:
        if event.get('httpMethod') == 'GET':
            return atlassianEndpoints()
        elif event.get('httpMethod') == 'POST':
            data = json.loads(event.get('body'))
            name = {
                "getAppNames": getAppNames(),
                "addApp": addApp(data),
                "reportIncident": reportIncident(data),
                "customFeed": getCustomEndpoints(data),
                "getStatus" : getStatus(data)
            }
            return name.get(data.get('action'), 'Invalid Method')
        else:
            raise Exception("Invalid Method")
    except Exception as e:
        return e
