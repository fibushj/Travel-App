from gui.gui_run import MainGUI
from models.initialization.initialization import initialize_db
import mysql.connector
from models.config import *


# TODO JHONNY: Database should be the only thing that modifies the database. When the GUI needs to send information to, or get information from the database, it can call methods on the database.
database = NotImplemented
gui = MainGUI(database)
gui.run()

# 
# #This code creates connection to MySql, and creates new data base for project


# mydb = mysql.connector.connect(
#     option_files='my.conf',
#     autocommit=True
# )
# cursor = mydb.cursor()
# cursor.execute('SET sql_mode = ""')

# initialize_db(cursor)

# cursor.close()

# mydb.close()