import mysql.connector
import models.queries.locations_screen as locations_screen
from models.utils import execute_sql_file
from models.config import *
import random
import csv


class Database:
    def initialize(self):
        self.mydb = mysql.connector.connect(
            option_files='my.conf',
            autocommit=True
        )
        self.cursor = self.mydb.cursor()

        # self.cursor.execute(f"""CREATE DATABASE {db_name}""")
        self.cursor.execute(f"USE {db_name}")
        # execute_sql_file(self.cursor, "models/initialization/tables_creation.sql")
        # execute_sql_file(self.cursor, "models/initialization/foreign_keys.sql")

        # self.populate_tables()
        # self.populate_users()
        # self.generate_reviews()
        self.cursor.execute(f"USE {db_name}")

    def close(self):
        self.cursor.close()
        self.mydb.close()

    def find_locations(self, country_name, radius, lat, lng, fclass, fcode, trip_type, trip_season, limit_size, last_id=0):
        query = ""
        if country_name == "":
            query += f""" 
                SET @R={radius};
                SET @earth_radius = 6378;
                SET @lat = {lat};
                SET @lng = {lng};
                SET @km_per_lat_degree = @earth_radius * PI() / 180;
                SET @lat_delta = @R /@km_per_lat_degree;
                SET @lng_delta = @lat_delta / COS(@lat * PI() / 180);
                SET @lat_min = @lat - @lat_delta;
                SET @lat_max = @lat + @lat_delta;
                SET @lng_min = @lng - @lng_delta;
                SET @lng_max = @lng + @lng_delta;
                """

        review_ignored_values = ["", "All"]
        review_conditions = ""
        if trip_season not in review_ignored_values:
            review_conditions += f"""
                    AND r.trip_season = (select id from trip_season where name = '{trip_season}')
                    """
        if trip_type not in review_ignored_values:
            review_conditions += f"""
                    AND r.trip_type = (select id from trip_type where name = '{trip_type}')
                    """

        query += f"""
                SELECT DISTINCT
                    l.id,
                    l.name,
                    lat latitude,
                    lng longitude,
                    (SELECT 
                            fclass.name
                        FROM
                            feature_code fcode
                                JOIN
                            feature_class fclass ON fcode.feature_class = fclass.id
                        WHERE
                            fcode.id = l.feature_code) category,
                    (SELECT 
                            fcode.name
                        FROM
                            feature_code fcode
                        WHERE
                            fcode.id = l.feature_code) subcategory,
                    (SELECT 
                            c.name
                        FROM
                            country c
                        WHERE
                            c.id = l.country_code) country,
                    (SELECT 
                            AVG(rating)
                        FROM
                            review r
                        WHERE
                            r.place_id = l.id
                            {review_conditions}
                            ) average_rating
                """
        if country_name != "":
            query += """
                    FROM
                        location l
                            JOIN
                        country c ON l.country_code = c.id
                    """
        else:
            query += """
            FROM location l
            """
        query += """
                    JOIN
                review r ON l.id = r.place_id
                """
        if country_name != "":
            query += f"""WHERE c.name = '{country_name}'
            """
        else:
            query += """
                    WHERE
                    lat between @lat_min and @lat_max and lng between @lng_min and @lng_max 
                    and (((ACOS(SIN(@lat * PI() / 180) * SIN(lat * PI() / 180) + COS(@lat * PI() / 180) * COS(lat * PI() / 180) * COS((@lng - lng) * PI() / 180)) * 180 / PI()) * 60 * 1.1515) * 1.609344) < @R
                    """
        if fclass != "":
            if fcode != "":
                query += f"""AND l.feature_code = (SELECT 
                                id
                            FROM
                                feature_code
                            WHERE
                                name ='{fcode}')
                        """
            else:
                query += f"""AND feature_code IN (SELECT 
                                fcode.id
                            FROM
                                feature_code fcode
                                    JOIN
                                feature_class fclass ON fcode.feature_class = fclass.id
                            WHERE
                                fclass.name = '{fclass}')
                """

        query += review_conditions
        query += f"""
                AND l.id > {last_id}
                ORDER BY l.id limit {limit_size}
                ;
                """
        return self.execute_query(query)

    def highest_rated_locations(self):
        query = """
                SELECT 
                    l.name,
                    lat latitude,
                    lng longitude,
                    (SELECT 
                            fclass.name
                        FROM
                            feature_code fcode
                                JOIN
                            feature_class fclass ON fcode.feature_class = fclass.id
                        WHERE
                            fcode.id = l.feature_code) category,
                    (SELECT 
                            fcode.name
                        FROM
                            feature_code fcode
                        WHERE
                            fcode.id = l.feature_code) subcategory,
                    (SELECT 
                            c.name
                        FROM
                            country c
                        WHERE
                            c.id = l.country_code) country,
                    temp.average_rating average_rating
                FROM
                    location l
                        JOIN
                    (SELECT 
                        place_id, AVG(rating) average_rating
                    FROM
                        review
                    GROUP BY place_id
                    ORDER BY average_rating DESC
                    LIMIT 20) temp ON l.id = temp.place_id;
            """
        return self.execute_query(query)

    def global_statistics(self):
        query = """
                SELECT 
                    trip_season,
                    trip_type,
                    FLOOR(YEAR(CURRENT_TIMESTAMP) - AVG(year_of_birth)) average_age
                FROM
                    (SELECT 
                        YEAR(date_of_birth) year_of_birth,
                            ttype.name trip_type,
                            tseason.name trip_season
                    FROM
                        trip_type ttype
                    JOIN review r ON ttype.id = r.trip_type
                    JOIN trip_season tseason ON tseason.id = r.trip_season
                    JOIN user u ON r.user_id = u.id
                    GROUP BY u.id , ttype.id , tseason.id) temp
                GROUP BY trip_type , trip_season
                ORDER BY trip_season , trip_type;
                """
        return self.execute_query(query)

    def trip_season_statistics_per_location(self, location_id):
        query=f"""
                SELECT 
                    (SELECT 
                            name
                        FROM
                            trip_season tseason
                        WHERE
                            id = trip_season) trip_season,
                    COUNT(*) num_reviews
                FROM
                    review
                WHERE
                    place_id = {location_id}
                GROUP BY trip_season;
            """
        return self.execute_query(query)

    def trip_type_statistics_per_location(self, location_id):
        query=f"""
                SELECT 
                    (SELECT 
                            name
                        FROM
                            trip_type ttype
                        WHERE
                            id = trip_type) trip_type,
                    COUNT(*) num_reviews
                FROM
                    review
                WHERE
                    place_id = {location_id}
                GROUP BY trip_type;
            """
        return self.execute_query(query)

    def execute_query(self, query):
        print(query)
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res


    # Function added by Anton
    # Those are simple functions that fetch necessary data for gui 
    def fetchCountries(self):
        self.cursor.execute("SELECT * FROM country;")
        return self.cursor.fetchall()

    def fetchFeatureClasses(self):
        self.cursor.execute("SELECT * FROM feature_class;")
        return self.cursor.fetchall()

    def fetchFeatureCodes(self, feature_class_name):
        self.cursor.execute(f"SELECT id FROM feature_class WHERE name = '{feature_class_name}';")
        feature_class_id = self.cursor.fetchall()[0][0]
        self.cursor.execute(f"SELECT * FROM feature_code WHERE feature_class = '{feature_class_id}';")
        return self.cursor.fetchall()

    def fetchTripSeasons(self):
        self.cursor.execute("SELECT * FROM trip_season;")
        return self.cursor.fetchall()

    def fetchTripTypes(self):
        self.cursor.execute("SELECT * FROM trip_type;")
        return self.cursor.fetchall()

    def fetchLocationReviews(self, location_id, limit):
        self.cursor.execute(f"SELECT * FROM review WHERE place_id = {location_id} LIMIT {limit};")
        return self.cursor.fetchall()

    def fetchUserReviews(self, user_id, limit):
        self.cursor.execute(f"SELECT * FROM review WHERE user_id = {user_id} LIMIT {limit};")
        return self.cursor.fetchall()

    # Those are functions needed for users handling
    def checkUserExistence(self, email, password):
        self.cursor.execute(f"SELECT * FROM user WHERE email = '{email}' AND password = '{password}';")
        query_result = self.cursor.fetchall()
        return query_result

    def checkEmailExistence(self, email):
        self.cursor.execute(f"SELECT COUNT(*) FROM user WHERE email = '{email}';")
        query_result = self.cursor.fetchall()[0][0]
        return query_result

    def enterNewUser(self, full_name, email, password, birth_date):
        self.cursor.execute(f"""INSERT INTO user(full_name, email, password, date_of_birth) 
                        VALUES('{full_name}', '{email}', '{password}', '{birth_date}');""")


    def countSpecificUserReviews(self, user_id, place_id, season_id):
        self.cursor.execute(f"""SELECT COUNT(*) FROM review WHERE user_id = {user_id} 
                                    AND place_id = {place_id} AND trip_season = {season_id};""")
        return self.cursor.fetchall()[0][0]

    def deleteUserReview(self, user_id, place_id, season_id):
        self.cursor.execute(f"""DELETE FROM review WHERE user_id = {user_id} 
                                    AND place_id = {place_id} AND trip_season = {season_id};""")

    def addUserReview(self, user_id, place_id, rating, trip_type, trip_season, anon_rew, text_rew):
        self.cursor.execute(f"""INSERT INTO review VALUES ({user_id},  {place_id}, 
                                    {rating}, {trip_type}, {trip_season}, {anon_rew}, '{text_rew}');""")

    # Functions for initial data base initialization
    def populate_tables(self):
        self.cursor.execute(f"""
        LOAD DATA INFILE '{feature_classes_path}'
        INTO TABLE feature_class
        FIELDS TERMINATED BY ':'
        enclosed by '"'
        LINES TERMINATED BY '\r\n' 
        IGNORE 1 LINES
        (id, name);      
        """)

        self.cursor.execute(f"""
        LOAD DATA INFILE '{feature_codes_path}'
        INTO TABLE feature_code
        FIELDS TERMINATED BY ','
        enclosed by '"'
        LINES TERMINATED BY '\r\n' 
        (@dummy, feature_class, id, name, description); 
        """)

        self.cursor.execute(f"""
        LOAD DATA INFILE '{country_codes_path}'
        INTO TABLE country
        FIELDS TERMINATED BY ','
        enclosed by '"'
        LINES TERMINATED BY '\r\n' 
        IGNORE 1 LINES
        (id, name);    
        """)

        self.cursor.execute(f"""
        LOAD DATA INFILE '{dataset_path}'
        INTO TABLE location
        FIELDS TERMINATED BY ','
        LINES TERMINATED BY '\n' 
        IGNORE 1 LINES
        (@geonameid,@asciiname,@latitude,@longitude,feature_code,country_code,population,elevation)
        set id=@geonameid, name=@asciiname, coordinates=POINT(@latitude, @longitude), elevation=if(@elevation="", null, @elevation);  
        """)

        self.cursor.execute(f"""
        LOAD DATA INFILE '{trip_types_path}'
        INTO TABLE trip_type
        FIELDS TERMINATED BY ','
        enclosed by '"'
        LINES TERMINATED BY '\r\n' 
        IGNORE 1 LINES
        (id, name);
        """)

        self.cursor.execute(f"""
        LOAD DATA INFILE '{trip_seasons_path}'
        INTO TABLE trip_season
        FIELDS TERMINATED BY ','
        enclosed by '"'
        LINES TERMINATED BY '\r\n' 
        IGNORE 1 LINES
        (id, name);
        """)

        self.cursor.execute(f""" 
        LOAD DATA INFILE '{reviews_path}'
        IGNORE INTO TABLE review
        FIELDS TERMINATED BY ','
        enclosed by ''
        LINES TERMINATED BY '\r\n' 
        (user_id, place_id, rating, trip_type, trip_season, anonymous_review, review); 
        """)

    def populate_users(self):
        command = [
            f'INSERT INTO {db_name}.user(full_name, email, password, date_of_birth) VALUES']
        first_names = []
        last_names = []

        with open('models/initialization/users_first_names.csv', newline='\r\n') as f:
            reader = csv.reader(f)
            for row in reader:
                first_names.append(row[0])
        with open('models/initialization/users_last_names.csv', newline='\r\n') as f:
            reader = csv.reader(f)
            for row in reader:
                last_names.append(row[0])

        for f_name in first_names:
            for l_name in last_names:
                full_name = f"{f_name} {l_name}"
                email = f"{l_name}.{f_name}@gmail.com"
                password = "123456"
                date_of_birth = self.generate_date()
                command.extend(
                    [f"('{full_name}', '{email}', '{password}', '{date_of_birth}')", ", "])

        command[-1] = ';'
        self.cursor.execute("".join(command))
        print("done")

    def generate_date(self):
        return f"{random.randint(1965, 2005)}-{random.randint(1, 12)}-{random.randint(1, 28)}"

    def generate_reviews(self):
        self.cursor.execute(
            'SELECT * FROM location WHERE country_code = "IL";')
        records = self.cursor.fetchall()
        self.write_reviews_set(records, [6, 10], [0, 40], [0, 10000])
        self.write_reviews_set(records, [1, 5], [0, 8], [10001, 20000])

    def write_reviews_set(self, places_list, ratings_range, reviews_range, users_range):
        with open('reviews.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            text_review = ["Terrible place", "Nothing remarkable", "Waste of time",
                           "Not bad at all", "Had a lot of fun", "The best place in the whole world"]

            for place_row in places_list:
                rewievs_num = random.randint(
                    reviews_range[0], reviews_range[1])
                user_id = random.randint(users_range[0], users_range[1])
                location_id = place_row[0]
                for _ in range(rewievs_num):
                    is_anonimous = random.randint(0, 1)
                    trip_type_id = random.randint(1, 10)
                    trip_season_id = random.randint(1, 4)
                    user_id += 1
                    rating = random.randint(ratings_range[0], ratings_range[1])
                    writer.writerow([user_id, location_id, rating, trip_type_id,
                                     trip_season_id, is_anonimous, text_review[rating//2]])
