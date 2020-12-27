from os import system
from models.utils import execute_sql_file
from models.config import *


def initialize_db(cursor):
    cursor.execute(f"""CREATE DATABASE {db_name}""")
    cursor.execute(f"USE {db_name}")
    execute_sql_file(cursor, "models/initialization/tables_creation.sql")
    execute_sql_file(cursor, "models/initialization/foreign_keys.sql")
    populate_tables(cursor)


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
    INTO TABLE Country
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


