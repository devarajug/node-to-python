import sys
import json
import psycopg2
from psycopg2.extras import RealDictCursor

def db_configure():
    conn = psycopg2.connect(
        host="localhost", #need to change to env
        database="NFRSecurity", #need to change to env
        user="pythonuser", #need to change to env
        password="R@manujan22", #need to change to env
        port=5432 #need to change to env
    )
    return conn

def Query(queryString, values=None):
    conn = None
    try:
        conn = db_configure()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        # print(queryString, values)
        cur.execute(queryString, values)

        result = json.dumps(cur.fetchall(), indent=2)
        result = json.loads(result)
        conn.close()
        return result
    except Exception as err:
        conn.close()
        return err

# print(Query("select exists (select table_catalog from information_schema.columns where table_schema = %s and table_name = %s)" ,['public', 'Authentication'])[0].get('exists'))
def Select(tableName, properties=None): #based on properies input need to change code.

    values = []
    queryString = "select table_catalog from " + tableName
    if properties:
        queryString = queryString + " where"
        for index, (propertyName, propertyValue) in enumerate(properties.items()):
            if index == 0:
                values.append(propertyValue)
                queryString = queryString + " " + propertyName + " = %s" #+ str(index+1)
            else:
                values.append(propertyValue)
                queryString = queryString + " and " + propertyName + " = %s" #+ str(index+1)

    # values = tuple(values)
    # print(values)
    result = Query(queryString=queryString, values=values)
    return result
    # return queryString

properties = {
    'table_schema' : 'public',
    'table_name' : 'AuthenticationApp_user'
}

# for row in Select(tableName="information_schema.columns", properties=properties):
#     print(row.get('table_catalog'))
