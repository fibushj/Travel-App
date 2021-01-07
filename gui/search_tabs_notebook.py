from tkinter import *
from tkinter import ttk
from ttkwidgets import TickScale
from gui.myFilterList import MyFilterList

FRAME_BG = '#80c1ff'

class SearchTabsNotebook(ttk.Notebook):
    def __init__(self,containing_frame):
        ttk.Notebook.__init__(self,containing_frame)
        # Create first tab in left frame- search by feature tab
        self.create_f_search_tab(containing_frame)
        # Create second tab in left frame- search by radius tab
        self.create_radius_search_tab(containing_frame)


    def create_filter_list(self,frame, source):
        filter_list = MyFilterList(frame, source=source, display_rule=lambda item: item,
                                   filter_rule=lambda item, text: text.lower() in item.lower())
        filter_list.pack(expand=True, fill=X)

        def show_result(event=None):
            item = filter_list.selection()
            if item: filter_list.set_entry_text(item)

        # Show the result of the calculation on Return or double-click
        filter_list.bind("<Return>", show_result)
        filter_list.bind("<Double-Button-1>", show_result)
        return filter_list


    # Create second tab in left frame- search by radius tab
    def create_trip_filter(self,frame):
        trip_frame = Frame(frame, bg=FRAME_BG, bd=3)
        trip_frame.pack(expand=True, fill=X)
        trip_type_val = StringVar()
        trip_season_val = StringVar()
        trip_type_options = ["Family", "Couples", "Solo"]
        trip_season_options = ["Spring", "Summer", "Fall", "Winter"]
        trip_type_dropmenu = ttk.OptionMenu(trip_frame, trip_type_val, "Trip type", "All", *trip_type_options)
        trip_season_dropmenu = ttk.OptionMenu(trip_frame, trip_season_val, "Trip season", "All", *trip_season_options)
        trip_type_dropmenu.config(width=10)
        trip_season_dropmenu.config(width=10)
        trip_type_dropmenu.pack(side="left", padx=3, expand=True, fill=X)
        trip_season_dropmenu.pack(side="right", padx=3, expand=True, fill=X)
        # trip_type_dropmenu.bind("<Return>", print_something)


    # Create first tab in left frame- search by feature tab
    def create_f_search_tab(self,containing_frame):
        f_search_tab = Frame(containing_frame, bg=FRAME_BG, bd=3)
        self.add(f_search_tab, text='Search By Country')

        country_frame = Frame(f_search_tab, bg=FRAME_BG, bd=3)
        country_frame.pack(expand=True, fill=X)
        country_label = Label(country_frame, text="Country:", anchor=W, bg=FRAME_BG).pack(expand=True, fill=X)
        #TODO JHONNY: fill list using query for all countries full name
        country_list_items = ["Denmark", "France", "Germany", "Israel", "United States", "United Kingdom"]
        country_filter_list = self.create_filter_list(country_frame, country_list_items)

        self.create_buttom_part(f_search_tab)

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
        radius_slider = TickScale(radius_frame, from_=0, to=1000,style="Horizontal.TScale", orient=HORIZONTAL, digits=0)
        radius_slider.pack(expand=True, fill=X)

        self.create_buttom_part(radius_search_tab)

    def create_buttom_part(self,containing_frame):
        f_class_frame = Frame(containing_frame, bg=FRAME_BG, bd=3)
        f_class_frame.pack(expand=True, fill=X)
        f_class_label = Label(f_class_frame, text="Feature Class:", anchor=W, bg=FRAME_BG).pack(expand=True, fill=X)
        # TODO JHONNY: fill list using query for all feature classes full name
        f_class_list_items = ["country, state, region...", "stream, lake...", "parks,area..."]
        f_class_filter_list = self.create_filter_list(f_class_frame, f_class_list_items)

        f_code_frame = Frame(containing_frame, bg=FRAME_BG, bd=3)
        f_code_frame.pack(expand=True, fill=X)
        f_code_label = Label(f_code_frame, text="Feature Code:", anchor=W, bg=FRAME_BG).pack(expand=True, fill=X)
        # TODO JHONNY: fill list using query for all feature codes full name that match the selected feature code
        f_code_list_items = ["Will change according to the feature class"]
        f_code_filter_list = self.create_filter_list(f_code_frame, f_code_list_items)

        trip_filter = self.create_trip_filter(containing_frame)

        # TODO JHONNY: query to get results using all filters and insert to locations_view
        f_submit_button = Button(containing_frame, text="Search", width=20, command=lambda: None)
        f_submit_button.pack(expand=True)