import mysql.connector
#from os import O_NONBLOCK, system
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


        
    def close(self): #TODO call it
        self.cursor.close()
        self.mydb.close()


    
    def locations_by_countries(cursor, fclass, fcode, trip_type, trip_season):
    #TODO type, season can be 'ALL'
        return NotImplemented



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
        command = [f'INSERT INTO {db_name}.user(full_name, email, password, date_of_birth) VALUES']
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
                command.extend([f"('{full_name}', '{email}', '{password}', '{date_of_birth}')", ", "])
        
        command[-1] = ';'
        self.cursor.execute("".join(command))
        print("done")

    def generate_date(self):
        return f"{random.randint(1965, 2005)}-{random.randint(1, 12)}-{random.randint(1, 28)}"




    def generate_reviews(self):
        self.cursor.execute('SELECT * FROM location WHERE country_code = "IL";')
        records = self.cursor.fetchall()
        self.write_reviews_set(records, [6,10], [0, 40], [0, 10000])
        self.write_reviews_set(records, [1,5], [0, 8], [10001, 20000])


    def write_reviews_set(self, places_list, ratings_range, reviews_range, users_range):
        with open('reviews.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            text_review = ["Terrible place", "Nothing remarkable", "Waste of time", "Not bad at all", "Had a lot of fun", "The best place in the whole world"]

            for place_row in places_list:
                rewievs_num = random.randint(reviews_range[0], reviews_range[1])
                user_id = random.randint(users_range[0], users_range[1])
                location_id = place_row[0]
                for _ in range(rewievs_num):
                    is_anonimous = random.randint(0,1)
                    trip_type_id = random.randint(1, 10)
                    trip_season_id = random.randint(1, 4)
                    user_id += 1
                    rating = random.randint(ratings_range[0], ratings_range[1])
                    writer.writerow([user_id, location_id, rating, trip_type_id, trip_season_id, is_anonimous, text_review[rating//2]])
        
