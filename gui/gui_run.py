#todo: refactor!

from tkinter import *
from tkinter import ttk

from gui.myFilterList import MyFilterList

HEIGHT = "768"
WIDTH = "1366"


def create_filter_list(frame, source):
    filter_list = MyFilterList(frame, source=source, display_rule=lambda item: item,
                                       filter_rule=lambda item, text: item.lower().startswith(text.lower()))
    filter_list.pack(expand=True, fill=X)

    def show_result(event=None):
        item = filter_list.selection()
        if item: filter_list.set_entry_text(item)

    # Show the result of the calculation on Return or double-click
    filter_list.bind("<Return>", show_result)
    filter_list.bind("<Double-Button-1>", show_result)
    return filter_list


# Create first tab in left frame- search by feature tab
def create_f_search_tab(left_frame):
    f_search_tab = Frame(left_frame, bg=left_frame_bg, bd=3)
    left_tabs_control.add(f_search_tab, text='Search By Country')

    country_frame = Frame(f_search_tab, bg=left_frame_bg, bd=3)
    country_frame.pack(expand=True, fill=X)
    country_label = Label(country_frame, text="Country:", anchor=W, bg=left_frame_bg).pack(expand=True, fill=X)
    country_list_items = ["Denmark", "France", "Germany", "Israel", "United States", "United Kingdom"]
    country_filter_list = create_filter_list(country_frame, country_list_items)

    # city_frame=Frame(f_search_tab, bg=left_frame_bg, bd=3)
    # city_frame.pack(expand=True, fill=X)
    # city_label= Label(city_frame,text="City:", anchor=W,bg=left_frame_bg).pack(expand=True, fill=X)
    # city_entry= Entry(city_frame).pack(expand=True, fill=X)

    f_class_frame = Frame(f_search_tab, bg=left_frame_bg, bd=3)
    f_class_frame.pack(expand=True, fill=X)
    f_class_label = Label(f_class_frame, text="Feature Class:", anchor=W, bg=left_frame_bg).pack(expand=True, fill=X)
    f_class_list_items = ["country, state, region...", "stream, lake...", "parks,area..."]
    f_class_filter_list = create_filter_list(f_class_frame, f_class_list_items)

    f_code_frame = Frame(f_search_tab, bg=left_frame_bg, bd=3)
    f_code_frame.pack(expand=True, fill=X)
    f_code_label = Label(f_code_frame, text="Feature Code:", anchor=W, bg=left_frame_bg).pack(expand=True, fill=X)
    f_code_list_items = ["Will change according to the feature class"]
    f_code_filter_list = create_filter_list(f_code_frame, f_code_list_items)

    trip_frame = Frame(f_search_tab, bg=left_frame_bg, bd=3)
    trip_frame.pack(expand=True, fill=X)
    trip_type_val = StringVar()
    trip_season_val = StringVar()
    trip_type_options = ["Family", "Couples", "Solo"]
    trip_season_options = ["Spring", "Summer", "Fall", "Winter"]
    trip_type_dropmenu = ttk.OptionMenu(trip_frame, trip_type_val, "Trip type", "All", *trip_type_options)
    trip_season_dropmenu = ttk.OptionMenu(trip_frame, trip_season_val, "Trip season", "All", *trip_season_options)
    trip_type_dropmenu.config(width=15)
    trip_season_dropmenu.config(width=15)
    trip_type_dropmenu.pack(side="left", padx=3, expand=True, fill=X)
    trip_season_dropmenu.pack(side="right", padx=3, expand=True, fill=X)
    # trip_type_dropmenu.bind("<Return>", print_something)

    f_submit_button = Button(f_search_tab, text="Search", width=20, command=lambda: None)
    f_submit_button.pack(expand=True)

#Create second tab in left frame- search by radius tab
def create_radius_search_tab(left_frame):
    radius_search_tab = Frame(left_frame, bg=left_frame_bg, bd=3)
    left_tabs_control.add(radius_search_tab, text='Search By Radius')

    lat_frame = Frame(radius_search_tab, bg=left_frame_bg, bd=3)
    lat_frame.pack(expand=True, fill=X)
    lat_label = Label(lat_frame, text="Latitude:", anchor=W, bg=left_frame_bg).pack(expand=True, fill=X)
    lat_entry = Entry(lat_frame).pack(expand=True, fill=X)

    lon_frame = Frame(radius_search_tab, bg=left_frame_bg, bd=3)
    lon_frame.pack(expand=True, fill=X)
    lon_label = Label(lon_frame, text="Longitude:", anchor=W, bg=left_frame_bg).pack(expand=True, fill=X)
    lon_entry = Entry(lon_frame).pack(expand=True, fill=X)

    radius_frame = Frame(radius_search_tab, bg=left_frame_bg, bd=3)
    radius_frame.pack(expand=True, fill=X)
    radius_label = Label(radius_frame, text="Radius:", anchor=W, bg=left_frame_bg).pack(expand=True, fill=X)
    radius_slider = Scale(radius_frame, from_=0, to=1000, orient=HORIZONTAL)
    radius_slider.pack(expand=True, fill=X)

    f_class_frame = Frame(radius_search_tab, bg=left_frame_bg, bd=3)
    f_class_frame.pack(expand=True, fill=X)
    f_class_label = Label(f_class_frame, text="Feature Class:", anchor=W, bg=left_frame_bg).pack(expand=True, fill=X)
    f_class_list_items = ["country, state, region...", "stream, lake...", "parks,area..."]
    f_class_filter_list = create_filter_list(f_class_frame, f_class_list_items)

    f_code_frame = Frame(radius_search_tab, bg=left_frame_bg, bd=3)
    f_code_frame.pack(expand=True, fill=X)
    f_code_label = Label(f_code_frame, text="Feature Code:", anchor=W, bg=left_frame_bg).pack(expand=True, fill=X)
    f_code_list_items = ["Will change according to the feature class"]
    f_code_filter_list = create_filter_list(f_code_frame, f_code_list_items)

    trip_frame = Frame(radius_search_tab, bg=left_frame_bg, bd=3)
    trip_frame.pack(expand=True, fill=X)
    trip_type_val = StringVar()
    trip_season_val = StringVar()
    trip_type_options = ["Family", "Couples", "Solo"]
    trip_season_options = ["Spring", "Summer", "Fall", "Winter"]
    trip_type_dropmenu = ttk.OptionMenu(trip_frame, trip_type_val, "Trip type", "All", *trip_type_options)
    trip_season_dropmenu = ttk.OptionMenu(trip_frame, trip_season_val, "Trip season", "All", *trip_season_options)
    trip_type_dropmenu.config(width=15)
    trip_season_dropmenu.config(width=15)
    trip_type_dropmenu.pack(side="left", padx=3, expand=True, fill=X)
    trip_season_dropmenu.pack(side="right", padx=3, expand=True, fill=X)
    # trip_type_dropmenu.bind("<Return>", print_something)

    radius_submit_button = Button(radius_search_tab, text="Search", width=20, command=lambda: None)
    radius_submit_button.pack(expand=True)


if __name__ == '__main__':
    root = Tk()
    root.title("Around The World")
    root.geometry(str(WIDTH) + 'x' + str(HEIGHT))

    # canvas = Canvas(root, height=HEIGHT, width=WIDTH)
    # canvas.pack()

    # background_image = PhotoImage(file='background.png')
    # background_label = Label(root, image=background_image)
    # background_label.place(relwidth=1, relheight=1)

    left_frame_bg = '#80c1ff'

    left_frame = Frame(root, bg=left_frame_bg, bd=3)
    left_frame.place(relx=0, rely=0, relwidth=0.2, relheight=1)

    # Create Tab Control
    left_tabs_control = ttk.Notebook(left_frame)

    # Create first tab in left frame- search by feature tab
    create_f_search_tab(left_frame)

    # Create second tab in left frame- search by radius tab
    create_radius_search_tab(left_frame)

    left_tabs_control.pack(expand=True, fill=BOTH)

    # Create right frame
    right_frame = Frame(root, bg=left_frame_bg, bd=10)
    right_frame.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)

    places_listbox = Listbox(right_frame, width=50)
    places_listbox.insert(1, "location1")
    places_listbox.insert(2, "location2")
    places_listbox.place(relwidth=1, relheight=1)

    root.mainloop()
