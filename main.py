from controller.db_manager import DataBaseManager
from models.database import Database
from gui.gui_run import MainGUI
from models.config import *


db = Database()
db.initialize()
# fclass, fcode, trip_type, trip_season = "city, village", "populated place", "", ""
# db.find_locations(country_name="", radius = 2, lat=32.109333, lng=34.855499, fclass=fclass, fcode=fcode, trip_type=trip_type, trip_season=trip_season, limit_size=50)
db_manager = DataBaseManager(db)
gui = MainGUI(db_manager)
gui.run()
db.close()