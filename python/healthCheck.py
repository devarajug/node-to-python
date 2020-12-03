import sys
import boto3
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
                "name":row.get('name'),
                "application_id":row.get('application_id'),
                "default_atlassian":row.get('default_atlassian'),
                "healthcheck_target":row.get('healthcheck_target')
            }
            defaultResults.append(temp)

        return defaultResults
    except Exception as err:
        return {
            'statusCode': 500,
            'message': "Error retrieving atlassian endpoints." + str(err)
        }

def getDetailGroup(data):
    try:
        incidentInfo = {
            "text" : "SELECT application_name, healthcheck_target, environment_type_id FROM status_master WHERE application_id = %s",
            "values" : [data.get('appID')]
        }
        details = Query(queryString=incidentInfo.get("text"), values=incidentInfo.get('values'))
        return details
    except Exception as err:
        return {
            'statusCode': 500,
            'message': "from getDetailsGroup Method Error getting past incidents. "+str(err)
        }

def getStatus(data):
    try:
        customOptions = {
            'timeout' : 3000
        }
        response = None
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
            return {
                'responseStatusCode': response.get('status'),
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

            return {
                'responseStatusCode': response.get('status'),
                'message': response.get('body'),
                'body': response
            }

    except Exception as err:
        return {
            'statusCode': 404,
            'message': "from getStatus method in healthcheck file error retrieving status code. "+ str(err)
        }
