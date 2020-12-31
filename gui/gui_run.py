from functools import partial
from tkinter import *
from tkinter import ttk
from gui.myFilterList import MyFilterList

HEIGHT = 768
WIDTH = 1366
LEFT_FRAME_BG= '#80c1ff'
RIGHT_FRAME_BG= '#80c1ff'

class MainGUI:

    def __init__(self, database):
        self.window = Tk()
        self.window.title("Around The World")
        self.window.geometry(str(WIDTH) + 'x' + str(HEIGHT))

        # canvas = Canvas(window, height=HEIGHT, width=WIDTH)
        # canvas.pack()

        # background_image = PhotoImage(file='background.png')
        # background_label = Label(window, image=background_image)
        # background_label.place(relwidth=1, relheight=1)

        left_frame = Frame(self.window, bg=LEFT_FRAME_BG, bd=3)
        left_frame.place(relx=0, rely=0, relwidth=0.2, relheight=1)

        # Create Tab Control
        left_tabs_control = ttk.Notebook(left_frame)

        # Create first tab in left frame- search by feature tab
        self.create_f_search_tab(left_frame,left_tabs_control)

        # Create second tab in left frame- search by radius tab
        self.create_radius_search_tab(left_frame,left_tabs_control)

        left_tabs_control.pack(expand=True, fill=BOTH)

        # Create right frame
        right_frame = Frame(self.window, bg=RIGHT_FRAME_BG, bd=10)
        right_frame.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)

        self.locations_view = ttk.Treeview(right_frame, selectmode='browse')
        self.locations_view['show'] = 'headings'
        self.locations_view["columns"] = ("1", "2", "3", "4", "5", "6", "7")
        self.locations_view.column("#0", width=0, minwidth=0, stretch=YES)
        self.locations_view.column("1", width=160, minwidth=80, stretch=YES)
        self.locations_view.column("2", width=80, minwidth=50, stretch=YES)
        self.locations_view.column("3", width=80, minwidth=50, stretch=YES)
        self.locations_view.column("4", width=80, minwidth=50, stretch=YES)
        self.locations_view.column("5", width=80, minwidth=50, stretch=YES)
        self.locations_view.column("6", width=80, minwidth=50, stretch=YES)
        self.locations_view.column("7", width=80, minwidth=50, stretch=YES)

        self.locations_view.heading("1", text="Name", anchor=W)
        self.locations_view.heading("2", text="Latitude", anchor=W)
        self.locations_view.heading("3", text="Longitude", anchor=W)
        self.locations_view.heading("4", text="Category", anchor=W)
        self.locations_view.heading("5", text="Sub Category", anchor=W)
        self.locations_view.heading("6", text="Country", anchor=W)
        self.locations_view.heading("7", text="Rating", anchor=W)

        # TODO JHONNY: insert all results that match the user's input, in this format:
        folder1 = self.locations_view.insert("", 1, None, values=(
        "Pic de Font Blanca", "42.64991", "1.53335", "...", "...", "Europe/Andorra", "4.5"))
        self.locations_view.bind("<Double-1>", self.location_double_click)
        self.locations_view.pack(expand=True, fill=BOTH)

        menu_widget = Menu(self.window)
        self.is_logged_in=False
        menu_widget.add_command(label="Profile", command=self.log_in if (not self.is_logged_in) else self.view_profile)
        menu_widget.add_command(label="Quit", command=self.window.quit)

        # display the menu
        self.window.config(menu=menu_widget)

    #TODO: implement!
    def validate_and_login(self,username, password):
        print("username entered :", username.get())
        print("password entered :", password.get())
        return

    def log_in(self):
        login_screen = Toplevel()
        login_screen.title("Login")
        login_screen.geometry("300x250")
        Label(login_screen, text="Please enter login details").pack()
        Label(login_screen, text="").pack()
        Label(login_screen, text="Username").pack()
        username = StringVar()
        username_login_entry = Entry(login_screen, textvariable=username)
        username_login_entry.pack()
        Label(login_screen, text="").pack()
        Label(login_screen, text="Password").pack()
        password = StringVar()
        password__login_entry = Entry(login_screen, textvariable=password, show='*')
        password__login_entry.pack()
        Label(login_screen, text="").pack()
        validate_and_login = partial(self.validate_and_login, username, password)
        Button(login_screen, text="Login", width=10, height=1,command=validate_and_login).pack()
        login_screen.mainloop()

    #TODO: implement!
    def view_profile(self):
        pass

    def run(self):
        self.window.mainloop()

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
        trip_frame = Frame(frame, bg=LEFT_FRAME_BG, bd=3)
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


    # Create first tab in left frame- search by feature tab
    def create_f_search_tab(self,left_frame,left_tabs_control):
        f_search_tab = Frame(left_frame, bg=LEFT_FRAME_BG, bd=3)
        left_tabs_control.add(f_search_tab, text='Search By Country')

        country_frame = Frame(f_search_tab, bg=LEFT_FRAME_BG, bd=3)
        country_frame.pack(expand=True, fill=X)
        country_label = Label(country_frame, text="Country:", anchor=W, bg=LEFT_FRAME_BG).pack(expand=True, fill=X)
        #TODO JHONNY: fill list using query for all countries full name
        country_list_items = ["Denmark", "France", "Germany", "Israel", "United States", "United Kingdom"]
        country_filter_list = self.create_filter_list(country_frame, country_list_items)

        f_class_frame = Frame(f_search_tab, bg=LEFT_FRAME_BG, bd=3)
        f_class_frame.pack(expand=True, fill=X)
        f_class_label = Label(f_class_frame, text="Feature Class:", anchor=W, bg=LEFT_FRAME_BG).pack(expand=True, fill=X)
        #TODO JHONNY: fill list using query for all feature classes full name
        f_class_list_items = ["country, state, region...", "stream, lake...", "parks,area..."]
        f_class_filter_list = self.create_filter_list(f_class_frame, f_class_list_items)

        f_code_frame = Frame(f_search_tab, bg=LEFT_FRAME_BG, bd=3)
        f_code_frame.pack(expand=True, fill=X)
        f_code_label = Label(f_code_frame, text="Feature Code:", anchor=W, bg=LEFT_FRAME_BG).pack(expand=True, fill=X)
        #TODO JHONNY: fill list using query for all feature codes full name that match the selected feature code
        f_code_list_items = ["Will change according to the feature class"]
        f_code_filter_list = self.create_filter_list(f_code_frame, f_code_list_items)

        trip_filter = self.create_trip_filter(f_search_tab)

        #TODO JHONNY: query to get results using all filters and insert to locations_view
        f_submit_button = Button(f_search_tab, text="Search", width=20, command=lambda: None)
        f_submit_button.pack(expand=True)


    def create_radius_search_tab(self,left_frame,left_tabs_control):
        radius_search_tab = Frame(left_frame, bg=LEFT_FRAME_BG, bd=3)
        left_tabs_control.add(radius_search_tab, text='Search By Radius')

        lat_frame = Frame(radius_search_tab, bg=LEFT_FRAME_BG, bd=3)
        lat_frame.pack(expand=True, fill=X)
        lat_label = Label(lat_frame, text="Latitude:", anchor=W, bg=LEFT_FRAME_BG).pack(expand=True, fill=X)
        lat_entry = Entry(lat_frame).pack(expand=True, fill=X)

        lon_frame = Frame(radius_search_tab, bg=LEFT_FRAME_BG, bd=3)
        lon_frame.pack(expand=True, fill=X)
        lon_label = Label(lon_frame, text="Longitude:", anchor=W, bg=LEFT_FRAME_BG).pack(expand=True, fill=X)
        lon_entry = Entry(lon_frame).pack(expand=True, fill=X)

        radius_frame = Frame(radius_search_tab, bg=LEFT_FRAME_BG, bd=3)
        radius_frame.pack(expand=True, fill=X)
        radius_label = Label(radius_frame, text="Radius:", anchor=W, bg=LEFT_FRAME_BG).pack(expand=True, fill=X)
        radius_slider = Scale(radius_frame, from_=0, to=1000, orient=HORIZONTAL)
        radius_slider.pack(expand=True, fill=X)

        f_class_frame = Frame(radius_search_tab, bg=LEFT_FRAME_BG, bd=3)
        f_class_frame.pack(expand=True, fill=X)
        f_class_label = Label(f_class_frame, text="Feature Class:", anchor=W, bg=LEFT_FRAME_BG).pack(expand=True, fill=X)
        #TODO JHONNY: fill list using query for all feature classes full name
        f_class_list_items = ["country, state, region...", "stream, lake...", "parks,area..."]
        f_class_filter_list = self.create_filter_list(f_class_frame, f_class_list_items)

        f_code_frame = Frame(radius_search_tab, bg=LEFT_FRAME_BG, bd=3)
        f_code_frame.pack(expand=True, fill=X)
        f_code_label = Label(f_code_frame, text="Feature Code:", anchor=W, bg=LEFT_FRAME_BG).pack(expand=True, fill=X)
        #TODO JHONNY: fill list using query for all feature codes full name that match the selected feature code
        f_code_list_items = ["Will change according to the feature class"]
        f_code_filter_list = self.create_filter_list(f_code_frame, f_code_list_items)

        trip_filter = self.create_trip_filter(radius_search_tab)

        #TODO JHONNY: query to get results using all filters and insert to locations_view
        radius_submit_button = Button(radius_search_tab, text="Search", width=20, command=lambda: None)
        radius_submit_button.pack(expand=True)


    def create_review_box(self, parent_frame, user_name, trip_season, review_text):

        frame = Frame(parent_frame, bg='blue', bd=0, highlightthickness=0)
        frame.pack(expand=True, fill= BOTH)

        canvas = Canvas(frame, bg=LEFT_FRAME_BG, width=50, height=50)
        canvas.create_text(8, 4, anchor=NW, fill="darkblue", font="Times 30 italic bold",
                           text=user_name[0])
        canvas.pack(side=LEFT, anchor=NW)
        text = Text(frame, bd=0,bg='pink')
        text.pack(side=LEFT, anchor=NW)

        text.tag_configure("sender", font="Arial 12 bold")
        text.tag_configure("message", font="Arial 10")  # , lmargin1=55, lmargin2=55)
        text.tag_configure("date", font="Arial 8")

        text.insert("end", user_name.title() + ' ', "sender")
        text.insert("end", trip_season + '\n', 'date')
        text.insert("end", '\n')  # Add a blank line to move next one down.
        text.insert("end", review_text + '\n\n', 'message')



    def location_double_click(self, event):
        item = self.locations_view.selection()[0]
        item_name=self.locations_view.item(item)["values"][0]
        item_window=Toplevel()
        item_window.title(item_name)
        item_window.geometry(str(int(WIDTH/2)) + 'x' + str(int(HEIGHT/2)))

        canvas = Canvas(item_window, borderwidth=0, background="orange")
        frame = Frame(canvas, background="red")
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        scrollbar = Scrollbar(item_window, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((4, 4), window=frame, anchor="nw")
        def onFrameConfigure(canvas):
            '''Reset the scroll region to encompass the inner frame'''
            canvas.configure(scrollregion=canvas.bbox("all"))
        frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        frame.bind_all("<MouseWheel>", _on_mousewheel)

        print("you clicked on", self.locations_view.item(item)["values"])

        user_name = 'Tom'
        trip_season = 'Summer'
        review_text = 'Hi Jim!\nwhassap\nwhassap\nwhassap\nwhassap\nwhassap\nwhassap\nwhassap\nwhassapgbfiusdiugfsdhgrdshgdfkjghljdfhg dhfkg hfdkjgh dsf kj dhfkhgkj fhgk hfdkg jktdth jdrf kgrtdfh grst hgkd hg dfhug dfhoh uuhgih rtdbhygrhtkj\nwhassap\nwhassap\nwhassap\nwhassap\nwhassap\nwhassap\nwhassap\nwhassap\nwhassap\nwhassap\nwhassap\nwhassap\nwhassap\nwhassap\nwhassap\nwhassap\nwhassap\nwhassap\nwhassap\nwhassap\nwhassap\nwhassap\nwhassap\nwhassap?'
        self.create_review_box(frame,user_name,trip_season,review_text)
        user_name1 = 'ghjngc'
        review_text1 = 'hi!!\n mannnnn'
        self.create_review_box(frame,user_name1,trip_season,review_text1)
