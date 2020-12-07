# import pandas
from initialization.tables_population import populate_tables
from initialization.tables_creation import create_tables
import mysql.connector

# This code creates connection to MySql, and creates new data base for project
mydb = mysql.connector.connect(
    option_files='my.conf'
)
cursor = mydb.cursor()
create_tables(cursor)
populate_tables(cursor)

mydb.close()



