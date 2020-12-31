
from gui.gui_run import run_gui
from models.initialization.initialization import initialize_db
import mysql.connector


#run_gui()
#This code creates connection to MySql, and creates new data base for project
mydb = mysql.connector.connect(
    option_files='my.conf',
    autocommit=True
)
cursor = mydb.cursor()
cursor.execute('SET sql_mode = ""')

initialize_db(cursor)


cursor.close()


mydb.close()



