# parametry połączenia

def connection_string():
    server = r'localhost\SQLEXPRESS'  # lub '127.0.0.1\SQLEXPRESS'
    database = 'Dane_scada'
    driver = '{ODBC Driver 17 for SQL Server}'

    connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

    return connection_string