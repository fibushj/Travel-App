from tkinter import *
from tkinter import ttk

from gui.gui_utils import create_scrollable_frame, create_review_box
from gui.pie_graph import PieGraph

FRAME_BG = '#80c1ff'
HEIGHT = 960
WIDTH = 1366

class LocationWindow(Toplevel):
    def __init__(self,item,item_name):
        Toplevel.__init__(self)

        self.title(item_name)
        self.geometry(str(int(WIDTH / 1.14)) + 'x' + str(int(HEIGHT / 2.2)))

        scrollable_frame = create_scrollable_frame(self)
        reviews_label = Label(scrollable_frame, text="Reviews:", anchor=W, bg=FRAME_BG, font=("Arial", 20)).pack(
            expand=True, fill=X)

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

        pie_frame = (ttk.Frame(self))
        pie_frame.pack(side="left", expand=False)
        pie_label = Label(pie_frame, text="Statistics:", anchor=W, bg=FRAME_BG, font=("Arial", 20)).pack(
            expand=True, fill=X)
        a = PieGraph(pie_frame)