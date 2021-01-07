from tkinter import *
from tkinter import ttk
from gui.location_window import LocationWindow

class LocationsView(ttk.Treeview):
    def __init__(self,containing_frame):
        ttk.Treeview.__init__(self,containing_frame, selectmode='browse')
        self['show'] = 'headings'
        self["columns"] = ("1", "2", "3", "4", "5", "6", "7")
        self.column("#0", width=0, minwidth=0, stretch=YES)
        self.column("1", width=160, minwidth=80, stretch=YES)
        self.column("2", width=80, minwidth=50, stretch=YES)
        self.column("3", width=80, minwidth=50, stretch=YES)
        self.column("4", width=80, minwidth=50, stretch=YES)
        self.column("5", width=80, minwidth=50, stretch=YES)
        self.column("6", width=80, minwidth=50, stretch=YES)
        self.column("7", width=80, minwidth=50, stretch=YES)

        self.heading("1", text="Name", anchor=W)
        self.heading("2", text="Latitude", anchor=W)
        self.heading("3", text="Longitude", anchor=W)
        self.heading("4", text="Category", anchor=W)
        self.heading("5", text="Sub Category", anchor=W)
        self.heading("6", text="Country", anchor=W)
        self.heading("7", text="Rating", anchor=W)

        # TODO JHONNY: insert all results that match the user's input, in this format:
        folder1 = self.insert("", 1, None, values=(
            "Pic de Font Blanca", "42.64991", "1.53335", "...", "...", "Europe/Andorra", "4.5"))
        self.bind("<Double-1>", self.location_double_click)
        self.pack(expand=True, fill=BOTH)

    def location_double_click(self, event):
        item = self.selection()[0]
        item_name = self.item(item)["values"][0]
        LocationWindow(item, item_name)