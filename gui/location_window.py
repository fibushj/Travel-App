from tkinter import *
from tkinter import ttk

from gui import consts
from gui.consts import WIDTH, HEIGHT, FRAME_BG
from gui.gui_utils import create_scrollable_frame, create_review_box
from gui.pie_graph import PieGraph

class LocationWindow(Toplevel):
    def __init__(self,item,item_name):
        Toplevel.__init__(self)

        self.title(item_name)
        self.geometry(str(int(WIDTH / 1.14)) + 'x' + str(int(HEIGHT / 1.08)))

        scrollable_frame = create_scrollable_frame(self)
        reviews_label = Label(scrollable_frame, text="Reviews:", anchor=W, bg=FRAME_BG, font=("Arial", 18)).pack(
            expand=True, fill=X)

        # possibility to add a review
        text = Text(scrollable_frame, bd=0, width=70, height=10 ,font=("Helvetica", "13"))
        text.pack(expand=True, fill=X)
        text.insert("end", ' Write your review here...')

        trip_season_val = StringVar()
        trip_season_dropmenu = ttk.OptionMenu(scrollable_frame, trip_season_val, "Trip season", "All", *consts.trip_season_options)
        trip_season_dropmenu.config(width=10)
        trip_season_dropmenu.pack(padx=3, expand=True)

        # TODO: add command
        add_review_button = Button(scrollable_frame, text="Add review", width=15, bg=FRAME_BG,
                                   command=lambda: None)
        add_review_button.pack(expand=True)

        # TODO JHONNY: query reviews for this item
        reviewer_name = 'Tom'
        trip_season = 'Summer'
        reviewer_birthday = {"year": 1995, "month": 3, "day": 28}
        review_text = 'The content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\n'
        create_review_box(scrollable_frame, reviewer_name, reviewer_birthday, trip_season, review_text)

        reviewer_name2 = 'Jhonny'
        review_text2 = 'The content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\n'
        reviewer_birthday2 = {"year": 2000, "month": 12, "day": 8}
        create_review_box(scrollable_frame, reviewer_name2, reviewer_birthday2, trip_season, review_text2)

        stats_frame = (ttk.Frame(self))
        stats_frame.pack(side="left", expand=False)

        #todo: query the amount of reviews on the current item for each trip type.
        trip_type_pie_label = Label(stats_frame, text="Trip Type Statistics:", anchor=W, bg=FRAME_BG, font=("Arial", 18)).pack(
            expand=True, fill=X)
        trip_type_labels = consts.trip_type_options
        trip_type_values = [30,50,28]
        trip_type_pie = PieGraph(stats_frame,trip_type_labels,trip_type_values)

        #todo: query the amount of reviews on the current item for each trip type.
        trip_season_pie_label = Label(stats_frame, text="Trip Season Statistics:", anchor=W, bg=FRAME_BG, font=("Arial", 18)).pack(
            expand=True, fill=X)
        trip_season_labels = consts.trip_season_options
        trip_season_values = [30,50,28,70]
        trip_type_pie = PieGraph(stats_frame,trip_season_labels,trip_season_values)