from tkinter import Toplevel, Label, X, Button, W, messagebox

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
        for review in user_reviews:
            place_id=review[1]
            trip_season = review[4]
            review_frame=create_review_box(containing_frame=scrollable_frame, location_name=review[0], reviewer_name="Me", rating=review[2], trip_type=review[3], trip_season=trip_season, reviewer_age="", review_text=review[6])
            def delete_handler(delete_button,place_id,trip_season):
                isSuc,err=db_manager.deleteCurrentUserReview(place_id,trip_season)
                if(isSuc):
                    review_frame.destroy()
                    delete_button.destroy()
                else:
                    messagebox.showinfo("Error", err)
            delete_button = Button(scrollable_frame, text="Delete", width=15, bg=FRAME_BG, command=lambda: delete_handler(delete_button,place_id,trip_season))
            delete_button.pack(expand=True)

