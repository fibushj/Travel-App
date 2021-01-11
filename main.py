from controller.db_manager import DataBaseManager
from models.database import Database
from gui.gui_run import MainGUI
from models.config import *

db = Database()
db.initialize()
db_manager = DataBaseManager(db)
gui = MainGUI(db_manager)
gui.run()
db.close()