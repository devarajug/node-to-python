import os
from db_utility_index import Query, Select
from api_utility_index import Get, Request


env_name = os.environ.get("HOOVER_ENV")
getEnvinormentID = {
    "DEV" : 3,
    "QA" : 2,
    "PROD" : 1
}
environment = getEnvinormentID.get(env_name)

def atlassianEndpoints():
    try:
        defaultResults = []
        getQuery = {
            "text" : "SELECT (SELECT name FROM application_master WHERE status_master.application_id = application_master.application_id), application_id, default_atlassian, environment_type_id, healthcheck_target FROM status_master WHERE default_atlassian = TRUE AND environment_type_id = $1 ORDER BY name",
            "values" : [environment]
        }
        response = Query(queryString=getQuery.get("text"), values=getQuery.get('values'))
        for row in response:
            temp = {
                "name":row[0],
                "application_id":row[1],
                "default_atlassian":row[2],
                "environment_type_id":row[3],
                "healthcheck_target":row[4]
            }
            defaultResults.append(temp)
        result = {
            'status':200,
            'body':defaultResults
        }
    except IndexError as ie:
        result = {"status":404, "body":"Atlasian Endpoints Query Result" + str(ie)}
    except Exception as err:
        result = {"status":404, "body":"Error retrieving atlassian endpoints." + str(err)}
    return result

def getDetailGroup(data):
    try:
        incidentInfo = {
            "text" : "SELECT application_name, healthcheck_target, environment_type_id FROM status_master WHERE application_id = %s",
            "values" : [data.get('appID')]
        }
        details = Query(queryString=incidentInfo.get("text"), values=incidentInfo.get('values'))
        result = details
    except Exception as err:
        result = "from getDetailsGroup Method Error getting past incidents. "+str(err)
    return result

def getStatus(data):
    try:
        customOptions = {
            'timeout' : 3000
        }
        if 'jenkins' in data.get('healthcheck_target'):
            response = Request(
                url=data.get("healthcheck_target"),
                method="GET",
                body=None,
                customHeaders={
                    'Authorization': {
                        'username':os.environ.get('jenkinsUsername'),
                        'password':os.environ.get('jenkinsPassword')
                    },
                    "Content-Type": "application/xml",
                    'Accept': "application/xml"
                }

            )
            result = {
                'statusCode': response.get('status'),
                'message': response.get('body'),
                'body': response
            }
        else:
            response = Request(
                url=data.get('healthcheck_target'),
                method="GET",
                body=None,
                customOptions=customOptions
            )

            result = response
    except Exception as err:
        result = {
            'statusCode': 404,
            'message': "from getStatus method in healthcheck file error retrieving status code. "+ str(err)
        }
    return result
