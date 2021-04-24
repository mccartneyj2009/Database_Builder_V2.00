import pyodbc
from deltaconnection import fetch_sites


def verify_dsn_source():
    sources = pyodbc.dataSources()
    dsns = sources.keys()
    data_source_list = []
    for key in dsns:
        data_source_list.append(key)
    if data_source_list.count("Delta ODBC 4") == 1:
        return True
    elif data_source_list.count("Delta ODBC 4") == 0:
        return False


def query_for_sites():
    connection = fetch_sites('Select SITE_ID from OBJECT_V4_NET')

    start_list_sites = []
    inter_list_sites = []
    final_list_sites = []

    for row in connection:
        start_list_sites.append(row)
    for i in start_list_sites:
        if i not in inter_list_sites:
            inter_list_sites.append(i)
    for site in inter_list_sites:
        final_list_sites.append(site[0])

    return final_list_sites


'''


def delete_points():
    pass'''
