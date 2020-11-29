import sys
import boto3
from db_utility_index import Query, Select
from api_utility_index import Get


class DBResults():

    def __init__(self, name, application_id, default_atlassian, environment_type_id, healthcheck_target):
        self.name = name,
        self.application_id = application_id,
        self.default_atlassian = default_atlassian
        self.environment_type_id = environment_type_id
        self.healthcheck_target = healthcheck_target


class AppNames():
    def __init__(self, name):
        self.name = name

getEnvironment = {
	"DEV":"3",
	"QA":"2",
    "PROD":"1",
}

environment = getEnvironment.get(process.env.HOOVER_ENV, "3")

def atkassianEndpoints():
    try:
        defaultResults = []
        getQuery = {
            "text" : "SELECT (select bane from application_master"
            "values" : [environment]
        }
        response = Query(queryString=getQuery.get("text"), values=getQuery.get('values'))

        for row in response:
            temp = DBResults(
                name=row.get('name'),
                application_id=row.get('application_id'),
                default_atlassian=row.get('default_atlassian'),
                environment_type_id = row.get('environment_type_id'),
                healthcheck_target=row.get('healthcheck_target')
            )
            defaultResults.append(temp)

        return defaultResults
    except Exception as err:
        return {
            'statusCode': 500,
            'message': "Error retrieving atlassian endpoints." + str(err)
        }

def getInternalID(data):
    internalIDQuery = {
		'text': "SELECT internal_id FROM user_master WHERE employee_id = %s",
		'values': [data.get('userID')]
	}
    internalID = Query(queryString=internalIDQuery.get('text'), internalIDQuery.get('values'))
    return internalID

def getCustomENdpoints(data):
    try:
        internalID = getInternalID(data)
        appOwnerQuery = {
            'text' : 'SELECT DISTINCT status_id FROM application_master Where internal_id = %s',
            'values' : [internalID[0].get('internal_id')]
        }
        appOwner = Query(queryString=appOwnerQuery.get('text'), values=appOwnerQuery.get('values'))
        if appOwner:
            appList = []
            for element in appOwnerQuery:
                appList.append(element.get('status_id'))
        applications = {
            'text': "SELECT DISTINCT application_name, application_master.application_id, environment_type_id, healthcheck_target FROM status_master LEFT OUTER JOIN application_master ON status_master.application_id = application_master.application_id WHERE application_master.application_id = ANY (&=%s) AND default_atlassian=FALSE ORDER BY environment_type_id, application_name",
            'values' : appList
        }
        return Query(applications.get('text'), applications.get('values'))
    except Exception as err:
        return {
            'statusCode': 500,
            'message': "ERROR retrieving application names. " + str(err)
        }

def checkDuplicateName(data):
    duplicate = {
        'text' : 'SELECT EXISTS (SELECT application_name FROM status_master WHERE application_name=%s)',
        'values' : [data.get('appName')]
    }

    if Query(duplicate)[0].get('exists'):
        return True
    else:
        return False

def checkDuplicateEndpoint(data):
    duplicate = {
        'text' : 'SELECT EXISTS (SELECT healthcheck_target FROM status_master WHERE healthcheck_target=%s)',
        'values' : [data.get('endpoint')]
    }

    if Query(duplicate)[0].get('exists'):
        return True
    else:
        return False

def getAppNames(data):
    try:
        results = []
        response = Query("SELECT name from application_master ORDER BY name")

        for row in response:
            temp = AppNames(row.get('name'))
            results.append(temp)
        return results
    except Exception as err:
        return {
            'statusCode': 500,
            'message': "Error retrieving appliacation names. " + str(err)
        }

def subscribeuser(data, status_id):
    internalID = getInternalID(data)

    insertOwnerQuery = {
        "text" : "INSERT INTO status_master_subscription(status_id, internal_id) VALUES(%s, %s)",
        "values" : [status_id, internalID[0].get('internal_id')]
    }

    insertOwner = Query(insertOwnerQuery.get('text'), insertOwnerQuery.get('values'))

    return insertOwner

def addApp(data):
    envType = None
    if data.environment == "PROD":
        envType = 1
    elif data.environment == "UAT":
        envType = 2
    else:
        envType = 3

    try:
        internalID = getInternalID(data)
        if data.get('newGroup'):
            #create new app group

            #create new sns topic
            pass
        else:
            appQuery = {
				'text': "SELECT application_id FROM status_master WHERE name=$1)",
				'values': [data.get('appGroup')],
			}
            appID = Query(appQuery.get('text'), appQuery.get('values'))

            insertQuery = {
                'text': "INSERT INTO status_master(application_id, default_atlassian, environment_type_id, healthcheck_target, slack_channel, application_name) VALUES(%s, %s, %s, %s, %s, %s) RETURNING status_id",
				'values': [appID[0].get('application_id'), False, envType, data.get('endpoint'), data.get('slack'), data.get('appName')],
            }
            insertStatus = Query(insertQuery.get('text'), insertQuery.get('values'))
            return subscribeUser(data, insertStatus)
    except Exception as err:
        return {
            'statusCode': 500,
            'message': "Error adding application. " + str(err)
        }

def reportIncident(data):
    try:
        idQuery = {
			'text': 'SELECT application_id From appliccation_master WHERE name = %s LIMIT 1',
			'values': [data.get('appGroup')],
		}

        getID = Query(idQuery.get('text'), idQuery.get('values'))

        insertQuery = {
			'text' : 'INSERT INTO incident_master(application_id, incident_title, incident_description, created) Values(%s, %s, %s, %s) RETURNING incident_id',
			'values' : [parseInt(getID[0].get('application_id')), data.get('title'), data.get('description'), data.get('timestamp')],
		}

        incidentID = Query(insertQuery.get('text'), insertQuery.get('values'))

        insertUserInfo = {
			'text': 'INSERT INTO incident_ownership(incident_id, user_id, first_name, last_name, email) Values($1, $2, $3, $4, $5) RETURNING *',
			'values': [parseInt(incidentID[0].get('incident_id')), data.get('userID'), data.get('firstName'), data.get('lastName'), data.email('email')],
		}

        return Query(insertUserInfo.get('text'), insertUserInfo.get('values'))

    except Exception as err:
        return {
            'statusCode': 500,
            'message': "Error getting past  incidents. " + str(err)
        }

def getIncidents(data):
    try:
        incidentInfo = {
            'text': "SELECT incident_title, incident_description, created  From incident_master WHERE created >= current_Timestamp - Interval '30' day and application_id= $s ORDER BY created DESC" ,
			'values': [data.get('appID')],
        }
        incidents = Query(incidentInfo.get('text'), incidentInfo.get('values'))
        return incidents
    except Exception as err:
        return {
            'statusCode': 500,
            'message': "Error getting past  incidents. " + str(err
        }

def getDetailGroup(data):
    try:
        detailsInfo = {
            'text': 'SELECT application_name, healthcheck_target, environment_type_id FROM status_master Where application_id = %s',
			'values': [data.get('appID')],
        }

        details = Query(detailsInfo.get('text'), detailsInfo.get('values'))
        return details
    except Exception as err:
        return {
            'statusCode': 500,
            'message': "error getting past incidents. " + str(err)
        }

def getStatus(data):
    try:
        customOptions = {
            'timeout' : 3000
        }
        response = Get(data.healthcheck_target, {}, customOptions)
        return {
            'statusCode': response.status,
            'message': "success",
            'body': response.body
        }
    except Exception as err:
        return {
            'statusCode': 404,
            'message': "error retrieving status code. "+ str(err)
        }
