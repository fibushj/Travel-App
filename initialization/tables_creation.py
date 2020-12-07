db_name = "sadna_project"

def create_tables(cursor):
    cursor.execute(f"""CREATE DATABASE {db_name}""")
    cursor.execute(f"USE {db_name}")
    cursor.execute("""
    CREATE TABLE locations (
        id INT PRIMARY KEY, 
        full_name VARCHAR(120) NOT NULL, 
        latitude DOUBLE NOT NULL, 
        longtitude DOUBLE NOT NULL, 
        feature_code VARCHAR(10) NOT NULL, 
        country_code VARCHAR(10) NOT NULL, 
        elevation INT 
    )"""
    )
    cursor.execute("""
    CREATE TABLE feature_codes( 
    feature_code VARCHAR(10) PRIMARY KEY, 
    full_name VARCHAR(120) NOT NULL, 
    feature_class VARCHAR(10) NOT NULL 
    )""")
    cursor.execute("""
    CREATE TABLE feature_classes( 
    feature_class VARCHAR(10) PRIMARY KEY, 
    full_name VARCHAR(120) NOT NULL 
    )""")
    cursor.execute("""
    CREATE TABLE countries( 
    country_code INT PRIMARY KEY, 
    full_name VARCHAR(40) NOT NULL 
    )""")
    cursor.execute("""
    CREATE TABLE users( 
    id INT AUTO_INCREMENT PRIMARY KEY, 
    full_name VARCHAR(80) NOT NULL, 
    date_of_birth DATETIME NOT NULL 
    )""")
    cursor.execute("""
    CREATE TABLE reviews( 
    user_id INT NOT NULL, 
    place_id INT NOT NULL, 
    rating INT NOT NULL, 
    trip_type VARCHAR(45), 
    trip_season VARCHAR(45) NOT NULL, 
    anonymous_review TINYINT, 
    review TINYTEXT, 
    PRIMARY KEY (user_id, place_id, trip_season)
    )""")    