from tkinter import *
from tkinter import ttk, messagebox

from gui import consts
from gui.consts import WIDTH, HEIGHT, FRAME_BG
from gui.gui_utils import create_scrollable_frame, create_review_box
from gui.pie_graph import PieGraph

class LocationWindow(Toplevel):
    def __init__(self,location,db_manager):
        Toplevel.__init__(self)

        self.title(location[1])
        self.geometry(str(int(WIDTH / 1.14)) + 'x' + str(int(HEIGHT / 1.08)))
        self.db_manager=db_manager
        scrollable_frame = create_scrollable_frame(self)
        reviews_label = Label(scrollable_frame, text="Reviews:", anchor=W, bg=FRAME_BG, font=("Arial", 18)).pack(
            expand=True, fill=X)

        # possibility to add a review
        text = Text(scrollable_frame, bd=0, width=70, height=10 ,font=("Helvetica", "13"))
        text.pack(expand=True, fill=X)
        text.insert("end", ' Write your review here...')

        trip_season_val = StringVar()
        trip_season_options,err = self.db_manager.fetchTripSeasons()
        trip_season_dropmenu = ttk.OptionMenu(scrollable_frame, trip_season_val, "Trip season", "All", *trip_season_options)
        trip_season_dropmenu.config(width=10)
        trip_season_dropmenu.pack(padx=3, expand=True)

        # TODO: add command
        add_review_button = Button(scrollable_frame, text="Add review", width=15, bg=FRAME_BG,
                                   command=lambda: None)
        add_review_button.pack(expand=True)
        location_id=location[0]
        location_reviews, err = db_manager.fetchLocationReviews(location_id,limit=50)
        for review in location_reviews:
            trip_season = review[5]
            reviewer_name = "Anonymous" if review[6] else review[0]
            review_frame = create_review_box(containing_frame=scrollable_frame, location_name="",
                                             reviewer_name=reviewer_name, rating=review[3], trip_type=review[4],
                                             trip_season=trip_season, reviewer_age=review[1], review_text=review[7])


        stats_frame = (ttk.Frame(self))
        stats_frame.pack(side="left", expand=False)

        trip_type_pie_label = Label(stats_frame, text=" Trip Type Statistics:", anchor=W, bg=FRAME_BG, font=("Arial", 18)).pack(
            expand=True, fill=X)
        trip_type_stats,err=db_manager.getLocationTripTypeStatistics(location_id)

        #split tuples list to labels and values
        trip_type_labels=[x[0] for x in trip_type_stats]
        trip_type_values =[x[1] for x in trip_type_stats]
        trip_type_pie = PieGraph(stats_frame,trip_type_labels,trip_type_values)

        trip_season_pie_label = Label(stats_frame, text=" Trip Season Statistics:", anchor=W, bg=FRAME_BG, font=("Arial", 18)).pack(
            expand=True, fill=X)
        trip_season_stats,err=db_manager.getLocationSeasonStatistics(location_id)
        #split tuples list to labels and values
        trip_season_labels=[x[0] for x in trip_season_stats]
        trip_season_values =[x[1] for x in trip_season_stats]
        trip_season_pie = PieGraph(stats_frame,trip_season_labels,trip_season_values)