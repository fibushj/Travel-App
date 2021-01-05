from os import system
from models.utils import execute_sql_file
from models.config import *
import random 
import csv


def initialize_db(cursor):
    #cursor.execute(f"""CREATE DATABASE {db_name}""")
    cursor.execute(f"USE {db_name}")
    #execute_sql_file(cursor, "models/initialization/tables_creation.sql")
    #execute_sql_file(cursor, "models/initialization/foreign_keys.sql")
    #populate_tables(cursor)
    populate_users(cursor)
    populate_reviews(cursor)


def populate_tables(cursor):
    cursor.execute(f"""
    LOAD DATA INFILE '{feature_classes_path}'
    INTO TABLE feature_class
    FIELDS TERMINATED BY ':'
    enclosed by '"'
    LINES TERMINATED BY '\r\n' 
	IGNORE 1 LINES
    (id, name);      
    """)   

     
    cursor.execute(f"""
    LOAD DATA INFILE '{feature_codes_path}'
    INTO TABLE feature_code
    FIELDS TERMINATED BY ','
    enclosed by '"'
    LINES TERMINATED BY '\r\n' 
    (@dummy, feature_class, id, name, description); 
    """)    

    cursor.execute(f"""
    LOAD DATA INFILE '{country_codes_path}'
    INTO TABLE country
    FIELDS TERMINATED BY ','
    enclosed by '"'
    LINES TERMINATED BY '\r\n' 
    IGNORE 1 LINES
    (id, name);    
    """)

    cursor.execute(f"""
    LOAD DATA INFILE '{dataset_path}'
    INTO TABLE location
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n' 
    IGNORE 1 LINES
    (@geonameid,@dummy,@asciiname,@dummy,@latitude,@longitude,@dummy,feature_code,country_code,@dummy,@dummy,@dummy,@dummy,@dummy,population,elevation,@dummy,@dummy,@dummy)
    set id=@geonameid, name=@asciiname, coordinates=POINT(@latitude, @longitude), elevation=if(@elevation="", null, @elevation);  
    """)

    cursor.execute(f"""
    LOAD DATA INFILE '{trip_types_path}'
    INTO TABLE trip_type
    FIELDS TERMINATED BY ','
    enclosed by '"'
    LINES TERMINATED BY '\r\n' 
    IGNORE 1 LINES
    (id, name);
    """)

    cursor.execute(f"""
    LOAD DATA INFILE '{trip_seasons_path}'
    INTO TABLE trip_season
    FIELDS TERMINATED BY ','
    enclosed by '"'
    LINES TERMINATED BY '\r\n' 
    IGNORE 1 LINES
    (id, name);
    """)


def populate_users(cursor):
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
            date_of_birth = generate_date()
            command.extend([f"('{full_name}', '{email}', '{password}', '{date_of_birth}')", ", "])
    
    command[-1] = ';'
    cursor.execute("".join(command))


def generate_date():
    return f"{random.randint(1965, 2005)}-{random.randint(1, 12)}-{random.randint(1, 28)}"


def populate_reviews(cursor):
    text_review = ["Terrible place", "Nothing remarkable", "Waste of time", "Not bad at all", "Had a lot of fun", "The best place in the whole world"]
    command = [f"INSERT INTO {db_name}.review(user_id, place_id, rating, trip_type, trip_season, anonymous_review, review) VALUES"]
    users_limit = 40000

    for user_id in range(users_limit):
        for _ in range(2):
            is_anonimous = random.randint(0,1)
            location_id = random.randint(870000, 1000000)
            trip_type_id = random.randint(1, 10)
            trip_season_id = random.randint(1, 4)
            rating = random.randint(1, 10)
            command.extend([f"({user_id}, {location_id}, {rating}, {trip_type_id}, {trip_season_id}, {is_anonimous}, '{text_review[rating//2]}')", ", "])
    
    command[-1] = ';'
    cursor.execute("".join(command))



