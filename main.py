from controller.db_manager import DataBaseManager
from models.database import Database
from gui.gui_run import MainGUI
from models.config import *


# TODO JHONNY: Database should be the only thing that modifies the database. When the GUI needs to send information to, or get information from the database, it can call methods on the database.
db = Database()
db.initialize()
fclass, fcode, trip_type, trip_season = "A", "PPL", "", ""
#db.find_locations(country_name="", radius = 2, lat=32.109333, lng=34.855499, fclass=fclass, fcode=fcode, trip_type=trip_type, trip_season=trip_season)
db_manager = DataBaseManager(db)
gui = MainGUI(db_manager)
gui.run()
db.close()