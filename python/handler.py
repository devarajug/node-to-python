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
            data = event.get('body')
            if data.get('action') == "getAppNames":
                return getAppNames(data)
            elif data.get('action') == "addApp":
                return addApp(data)
            elif data.get('action') == "reportIncident":
                return reportIncident(data)
            elif data.get('action') == "customFeed":
                return getCustomEndpoints(data)
            elif data.get("action") == "getStatus":
                return getStatus(data)
            else:
                raise Exception("Invalid Method")
        else:
            raise Exception("Invalid Method")

    except Exception as e:
        return str(e)
