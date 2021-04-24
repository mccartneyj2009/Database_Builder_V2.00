import pyodbc


def make_connection(sql_statement='Select SITE_ID from OBJECT_V4_NET'):
    dsn = 'DSN=Delta ODBC 4'
    autocommit = True
    cnxn = pyodbc.connect(dsn, autocommit=autocommit)
    cursor = cnxn.cursor()
    cursor.execute(sql_statement)
    cursor.close()
    cnxn.close()


def fetch_sites(sql_statement='Select SITE_ID from OBJECT_V4_NET'):
    sql_query_returned_list = []
    dsn = 'DSN=Delta ODBC 4'
    autocommit = True
    cnxn = pyodbc.connect(dsn, autocommit=autocommit)
    cursor = cnxn.cursor()
    for i in cursor.execute(sql_statement):
        sql_query_returned_list.append(i)
    cursor.close()
    cnxn.close()
    return sql_query_returned_list


def fetch_points(sql_statement):
    result =[]
    dsn = 'DSN=Delta ODBC 4'
    autocommit = True
    cnxn = pyodbc.connect(dsn, autocommit=autocommit)
    cursor = cnxn.cursor()
    cursor.execute(sql_statement)
    for item in cursor.fetchall():
        result.append(item)
    cursor.close()
    cnxn.close()
    return result
