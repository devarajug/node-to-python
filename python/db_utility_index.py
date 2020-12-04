import os
import json
import psycopg2

PG_Config = {
    'user':'pythonuser', #os.environ.get("PG_USERNAME"),
    'password':'R@manujan22', #os.environ.get("PG_PASSWORD"),
    'database':'NFRSecurity', #os.environ.get("PG_DB_NAME"),
    'host':'127.0.0.1', #os.environ.get("PG_HOST"),
    'port':5432, #os.environ.get("PG_PORT")
    'sslmode':'require'
}

def Query(queryString, values=None):
    conn = None
    try:
        with psycopg2.connect(**PG_Config) as conn:
            cur = conn.cursor()
            cur.execute(queryString, values)
            result = cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as err:
        result = str(err)

    return result

# print(Query("select exists (select table_catalog from information_schema.columns where table_schema = %s and table_name = %s)" ,['public', 'Authentication']))

def Select(tableName, properties=None):

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

    result = Query(queryString=queryString, values=values)
    return result
