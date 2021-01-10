from tkinter import *
from tkinter import ttk
from ttkwidgets import TickScale

from gui import consts
from gui.consts import FRAME_BG
from gui.my_filter_list import MyFilterList


class SearchTabsNotebook(ttk.Notebook):
    def __init__(self,containing_frame, db_manager, locations_view):
        self.db_manager=db_manager
        self.locations_view=locations_view
        ttk.Notebook.__init__(self,containing_frame)
        # Create first tab in left frame- search by feature tab
        self.create_f_search_tab(containing_frame)
        # Create second tab in left frame- search by radius tab
        self.create_radius_search_tab(containing_frame)

    # Create first tab in left frame- search by feature tab
    def create_f_search_tab(self,containing_frame):
        f_search_tab = Frame(containing_frame, bg=FRAME_BG, bd=3)
        self.add(f_search_tab, text='Search By Country')

        country_frame = Frame(f_search_tab, bg=FRAME_BG, bd=3)
        country_frame.pack(expand=True, fill=X)
        country_label = Label(country_frame, text="Country:", anchor=W, bg=FRAME_BG).pack(expand=True, fill=X)
        country_list_items,err = self.db_manager.fetchCountries()
        self.country_filter_list = self.create_filter_list(country_frame, country_list_items)

        self.create_buttom_part(f_search_tab)


    def create_buttom_part(self,containing_frame):
        f_class_frame = Frame(containing_frame, bg=FRAME_BG, bd=3)
        f_class_frame.pack(expand=True, fill=X)
        f_class_label = Label(f_class_frame, text="Feature Class:", anchor=W, bg=FRAME_BG).pack(expand=True, fill=X)
        f_class_list_items,err = self.db_manager.fetchFeatureClasses()
        self.f_class_filter_list = self.create_filter_list(f_class_frame, f_class_list_items)

        f_code_frame = Frame(containing_frame, bg=FRAME_BG, bd=3)
        f_code_frame.pack(expand=True, fill=X)
        f_code_label = Label(f_code_frame, text="Feature Code:", anchor=W, bg=FRAME_BG).pack(expand=True, fill=X)
        f_code_list_items = ["Please choose feature class first!"]
        self.f_code_filter_list = self.create_filter_list(f_code_frame, f_code_list_items)

        trip_filter = self.create_trip_filter(containing_frame)

        f_submit_button = Button(containing_frame, text="Search", width=20, command=self.f_search_and_update_locations)
        f_submit_button.pack(expand=True)


    def create_filter_list(self,frame, source):
        filter_list = MyFilterList(frame, source=source, display_rule=lambda item: item,
                                   filter_rule=lambda item, text: text.lower() in item.lower())
        filter_list.pack(expand=True, fill=X)

        def show_result(event=None):
            item = filter_list.selection()
            if item:
                filter_list.set_entry_text(item)

        # Show the result of the calculation on Return or double-click
        # TODO: for feature codes only- fill list using query for all feature codes full name that match the selected feature class
        filter_list.bind("<Return>", show_result)
        filter_list.bind("<Double-Button-1>", show_result)
        return filter_list

    # Create second tab in left frame- search by radius tab
    def create_trip_filter(self,frame):
        trip_frame = Frame(frame, bg=FRAME_BG, bd=3)
        trip_frame.pack(expand=True, fill=X)
        self.trip_type_val = StringVar()
        self.trip_season_val = StringVar()
        trip_type_options,err = self.db_manager.fetchTripTypes()
        trip_season_options,err = self.db_manager.fetchTripSeasons()
        trip_type_dropmenu = ttk.OptionMenu(trip_frame, self.trip_type_val, "Trip type", "All", *trip_type_options, command=lambda selection: self.trip_type_val.set(selection))
        trip_season_dropmenu = ttk.OptionMenu(trip_frame, self.trip_season_val, "Trip season", "All", *trip_season_options, command=lambda selection: self.trip_season_val.set(selection))
        trip_type_dropmenu.config(width=10)
        trip_season_dropmenu.config(width=10)
        trip_type_dropmenu.pack(side="left", padx=3, expand=True, fill=X)
        trip_season_dropmenu.pack(side="right", padx=3, expand=True, fill=X)
        # trip_type_dropmenu.bind("<Return>", print_something)

    def f_search_and_update_locations(self):
        country_choice=self.country_filter_list.selection()
        f_class_choice=self.f_class_filter_list.selection()
        # f_code_choice=self.f_code_filter_list.selection()
        f_code_choice="populated place"
        trip_type_choice=self.trip_type_val.get()
        trip_season_choice=self.trip_season_val.get()
        # TODO: query to get results using all filters and insert to locations_view
        results,err=self.db_manager.searchLocations(country_name=country_choice,fclass=f_class_choice,fcode=f_code_choice,trip_type=trip_type_choice,trip_season=trip_season_choice,radius=None,lat=None,lng=None,limit_size=50)

        self.locations_view.clear_table()
        # TODO: insert all results that match the user's input, in this format:
        self.locations_view.insert_row(("Pic de Font Blanca", "42.64991", "1.53335", "...", "...", "Europe/Andorra", "4.5"))





    def create_radius_search_tab(self,containing_frame):
        radius_search_tab = Frame(containing_frame, bg=FRAME_BG, bd=3)
        self.add(radius_search_tab, text='Search By Radius')

        lat_frame = Frame(radius_search_tab, bg=FRAME_BG, bd=3)
        lat_frame.pack(expand=True, fill=X)
        lat_label = Label(lat_frame, text="Latitude:", anchor=W, bg=FRAME_BG).pack(expand=True, fill=X)
        lat_entry = Entry(lat_frame)
        lat_entry.pack(expand=True, fill=X)

        lon_frame = Frame(radius_search_tab, bg=FRAME_BG, bd=3)
        lon_frame.pack(expand=True, fill=X)
        lon_label = Label(lon_frame, text="Longitude:", anchor=W, bg=FRAME_BG).pack(expand=True, fill=X)
        lon_entry = Entry(lon_frame)
        lon_entry.pack(expand=True, fill=X)

        radius_frame = Frame(radius_search_tab, bg=FRAME_BG, bd=3)
        radius_frame.pack(expand=True, fill=X)
        radius_label = Label(radius_frame, text="Radius:", anchor=W, bg=FRAME_BG).pack(expand=True, fill=X)
        ttk.Style().configure('Horizontal.TScale', background=FRAME_BG) # define a style object for the scale widget
        radius_slider = TickScale(radius_frame, from_=0, to=100,style="Horizontal.TScale", orient=HORIZONTAL, digits=0)
        radius_slider.pack(expand=True, fill=X)

        self.create_buttom_part(radius_search_tab)

