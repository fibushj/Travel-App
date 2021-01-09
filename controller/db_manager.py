import mysql.connector
from models.database import Database
from controller.utils import generateErrorMessage

class DataBaseManager:

    def __init__(self, database):
        self.database = database
        self.user_logged_in = False
        self.user_data = None



    ### - FETCH OVERALL DATA FUNCTIONS
    def fetchCountries(self):
        try:
            result = self.database.fetchCountries()
            return result, None
        except Exception as err:
                return None, generateErrorMessage(err.args[0])

    def fetchFeatureClasses(self):
        try:
            result = self.database.fetchFeatureClasses()
            return result, None
        except Exception as err:
                return None, generateErrorMessage(err.args[0])

    def fetchFeatureCodes(self):
        try:
            result = self.database.fetchFeatureCodes()
            return result, None
        except Exception as err:
                return None, generateErrorMessage(err.args[0])

    def fetchTripSeasons(self):
        try:
            result = self.database.fetchTripSeasons()
            return result, None
        except Exception as err:
                return None, generateErrorMessage(err.args[0])

    def fetchTripTypes(self):
        try:
            result = self.database.fetchTripTypes()
            return result, None
        except Exception as err:
                return None, generateErrorMessage(err.args[0])


    def fetchLocationReviews(self, location_id, limit):
        try:
            result = self.database.fetchLocationReviews(location_id, limit)
            return result, None
        except Exception as err:
                return None, generateErrorMessage(err.args[0])


    ### - USER RELATED FUNCTIONS
    def logInUser(self, email, password):
        try:
            if self.user_logged_in:
                return False, "User already logged in"

            query_result = self.database.checkUserExistence(email, password)
            if(len(query_result) > 0):
                self.user_data = query_result[0]
                self.user_logged_in = True
                return True, None
            else:
                return False, "Such user not exist"
        except Exception as err:
                return False, generateErrorMessage(err.args[0])


    def logOutUser(self):
        if self.user_logged_in:
            self.user_logged_in = False
            return True, None
        else:
            return False, "User was not logged in"


    def _validateUserEnryData(self, email):
        query_result = self.database.checkEmailExistence(email)
        if query_result > 0:
            return True
        else:
            return False


    def registerUser(self, full_name, email, password, birth_date):
        try:
            if self._validateUserEnryData(email):
                return False, "Such email already taken"
            else:
                self.database.enterNewUser(full_name, email, password, birth_date)
                self.logInUser(email, password)
                return True, None
        except Exception as err:
                return False, generateErrorMessage(err.args[0])

    
    def isUserLoggedIn(self):
        return self.user_logged_in
    

    def getCurrentUserReviews(self, limit):
        try:
            if self.user_logged_in:
                result = self.database.fetchUserReviews(self.user_data[0], limit)
                return result, None
            else:
                return None, "You had not logged in"
        except Exception as err:
                return None, generateErrorMessage(err.args[0])

    def _isReviewBelongsToUser(self, place_id, season_id):
        if self.isUserLoggedIn():
            if self.database.countSpecificUserReviews(self.user_data[0], place_id, season_id) > 0:
                return True
            else:
                return False
        else:
            return False
    

    def deleteCurrentUserReview(self, place_id, season_id):
        try:
            if self.isUserLoggedIn() and self._isReviewBelongsToUser(place_id, season_id):
                self.database.deleteUserReview(self.user_data[0], place_id, season_id)
                return True, None
            elif not self.isUserLoggedIn():
                return False, "You had not logged in"
            else:
                return False, "Review was not written by user"
        except Exception as err:
                return False, generateErrorMessage(err.args[0])
    

    def addCurrentUserReview(self, place_id, rating, trip_type, trip_season, anon_rew, text_rew):
        try:
            if self.isUserLoggedIn() and (rating <= 10 and rating >= 1) and ((type(text_rew) == type('')) and (len(text_rew) < 300)):
                self.database.addUserReview(self.user_data[0], place_id, rating, trip_type, trip_season, anon_rew, text_rew)
                return True, None
            elif not self.isUserLoggedIn():
                return False, "You had not logged in"
            elif not (rating <= 10 and rating >= 1):
                return False, "Rating must be value between 1 and 10"
            elif not ((type(text_rew) == type('')) and (len(text_rew) < 300)):
                return False, "Text review must be less that 300 characters"
        except Exception as err:
                return False, generateErrorMessage(err.args[0])
    
    
    # def isLocationReviewedByUser(self, place_id):
    #     try:
    #         if self.isUserLoggedIn():
    #             self.cursor.execute(f"SELECT COUNT(*) FROM review WHERE user_id = {self.user_data[0]} AND place_id = {place_id};")
    #             result_list = self.cursor.fetchall()
    #             if result_list[0][0] > 0:
    #                 return True, None
    #             else:
    #                 return False, "User not viewed current location"
    #         else:
    #             return False, "You had not logged in"
    #     except Exception as err:
    #             return False, generateErrorMessage(err.args[0])


