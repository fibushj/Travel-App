import mysql.connector
from models.config import *

class DataBaseManager:

    def __init__(self):
        self.mydb = mysql.connector.connect(
            option_files='my.conf',
            autocommit=True
        )
        self.cursor = self.mydb.cursor()
        self.cursor.execute('SET sql_mode = ""')
        self.user_logged_in = False
        self.user_data = None
        self.cursor.execute(f"USE {db_name}")



    ### - FETCH OVERALL DATA FUNCTIONS
    def fetchCountries(self):
        self.cursor.execute("SELECT * FROM country;")
        return self.cursor.fetchall()

    def fetchFeatureClasses(self):
        self.cursor.execute("SELECT * FROM feature_class;")
        return self.cursor.fetchall()

    def fetchFeatureCodes(self):
        self.cursor.execute("SELECT * FROM feature_code;")
        return self.cursor.fetchall()




    ### - SEARCH QUERIES FUNCTIONS
    #TODO: add args
    def fetchLocationsCountriesMode(self):
        self.cursor.execute("SELECT * FROM location LIMIT 100;")
        return self.cursor.fetchall()

    #TODO: add args
    def fetchLocationsCoordsMode(self):
        self.cursor.execute("SELECT * FROM location LIMIT 100;")
        return self.cursor.fetchall()



    def fetchLocationReviews(self, location_id):
        self.cursor.execute(f"SELECT * FROM review WHERE place_id = {location_id} LIMIT 50;")
        return self.cursor.fetchall()

    #TODO: add function contents
    def fetchLocationStatistics(self, location_id):
        return None




    ### - USER RELATED FUNCTIONS
    def logInUser(self, email, password):
        if self.user_logged_in:
            return False

        self.cursor.execute(f"SELECT * FROM user WHERE email = '{email}' AND password = '{password}';")
        query_result = self.cursor.fetchall()
        if(len(query_result) > 0):
            self.user_data = query_result[0]
            self.user_logged_in = True
            return True
        else:
            return False


    def logOutUser(self):
        if self.user_logged_in:
            self.user_logged_in = False
            return True
        else:
            return False


    def _validateUserEnryData(self, email):
        self.cursor.execute(f"SELECT COUNT(*) FROM user WHERE email = '{email}';")
        query_result = self.cursor.fetchall()[0][0]
        if query_result > 0:
            return True
        else:
            return False

    
    def registerUser(self, full_name, email, password, birth_date):
        if self._validateUserEnryData(email):
            return False
        else:
            self.cursor.execute(f"INSERT INTO user(full_name, email, password, date_of_birth) VALUES('{full_name}', '{email}', '{password}', '{birth_date}');")
            self.logInUser(email, password)
            return True

    
    def isUserLoggedIn(self):
        return self.user_logged_in
    
    def getCurrentUserReviews(self):
        if self.user_logged_in:
            self.cursor.execute(f"SELECT * FROM review WHERE user_id = {self.user_data[0]} LIMIT 50;")
            return self.cursor.fetchall()
        else:
            return None
    
    def isReviewBelongsToUser(self, place_id, season_id):
        if self.isUserLoggedIn():
            self.cursor.execute(f"SELECT COUNT(*) FROM review WHERE user_id = {self.user_data[0]} AND place_id = {place_id} AND trip_season = {season_id};")
            if self.cursor.fetchall()[0][0] > 0:
                return True
            else:
                return False
        else:
            False
    
    def deleteCurrentUserReview(self, place_id, season_id):
        if self.isUserLoggedIn() and self.isReviewBelongsToUser(place_id, season_id):
            self.cursor.execute(f"""DELETE FROM review WHERE user_id = {self.user_data[0]} 
                                    AND place_id = {place_id} AND trip_season = {season_id};""")
            return True
        else:
            return False
    
    def addCurrentUserReview(self, place_id, rating, trip_type, trip_season, anon_rew, text_rew):
        if self.isUserLoggedIn() and (rating <= 10 and rating >= 1) and (type(text_rew) == type('')) and (len(text_rew) < 300):
            try:
                self.cursor.execute(f"""INSERT INTO review VALUES ({self.user_data[0]},  {place_id}, 
                                        {rating}, {trip_type}, {trip_season}, {anon_rew}, '{text_rew}');""")
            except Exception as err:
                raise Exception(generateErrorMessage(err.args[0]))
            return True
        else:
            return False
    
    def isLocationReviewedByUser(self, place_id):
        if self.isUserLoggedIn():
            self.cursor.execute(f"SELECT COUNT(*) FROM review WHERE user_id = {self.user_data[0]} AND place_id = {place_id};")
            result_list = self.cursor.fetchall()
            if result_list[0][0] > 0:
                return True
            else:
                return False
        else:
            False




    ### - Pagination Functions
    def fetchProceedingDataFromLastQuery(self):
        return None


def generateErrorMessage(error_number):
    if error_number == 1062:
        return "You already wrote review for such trip."