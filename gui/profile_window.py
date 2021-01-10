from tkinter import Toplevel, Label, X, Button, W

from gui.consts import FRAME_BG, WIDTH, HEIGHT
from gui.gui_utils import create_scrollable_frame, create_review_box

class ProfileWindow(Toplevel):
    def __init__(self,db_manager):
        Toplevel.__init__(self)
        self.title("My Profile")
        self.geometry(str(int(WIDTH / 1.75)) + 'x' + str(int(HEIGHT / 2)))

        scrollable_frame = create_scrollable_frame(self)
        reviews_label = Label(scrollable_frame, text="Reviews:", anchor=W, bg=FRAME_BG, font=("Arial", 18)).pack(
            expand=True, fill=X)

        user_reviews,err=db_manager.getCurrentUserReviews(limit=50)
        # TODO JHONNY: query reviews for this user
        reviewer_name = 'Me'
        trip_season = 'Summer'
        reviewer_birthday = {"year": 1995, "month": 3, "day": 28}
        review_text = 'The content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\n'
        create_review_box(scrollable_frame, reviewer_name, reviewer_birthday, trip_season, review_text)

        # TODO JHONNY: delete the review whose delete button was pressed
        delete_button = Button(scrollable_frame, text="Delete", width=15, bg=FRAME_BG, command=lambda: None)
        delete_button.pack(expand=True)

        reviewer_name2 = 'Me'
        review_text2 = 'The content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\nThe content of the review...\n'
        reviewer_birthday2 = {"year": 2000, "month": 12, "day": 8}
        create_review_box(scrollable_frame, reviewer_name2, reviewer_birthday2, trip_season, review_text2)

        delete_button2 = Button(scrollable_frame, text="Delete", width=15, bg=FRAME_BG, command=lambda: None)
        delete_button2.pack(expand=True)