from models.model import Model
from gui.gui_run import MainGUI
from models.initialization.initialization import initialize_db
from models.config import *


# TODO JHONNY: Database should be the only thing that modifies the database. When the GUI needs to send information to, or get information from the database, it can call methods on the database.
model = Model()
#model.initialize()
database = NotImplemented
gui = MainGUI(database)
gui.run()
model.close()



