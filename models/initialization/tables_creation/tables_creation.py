db_name = "sadna_project"


def create_tables(cursor):
    #TODO change the following line
    cursor.execute("""
    DROP DATABASE IF EXISTS `sadna`; 
    """)
    cursor.execute(f"""CREATE DATABASE {db_name}""")
    cursor.execute(f"USE {db_name}")

    cursor.execute("""
    CREATE TABLE countries( 
    country_code VARCHAR(10) PRIMARY KEY, 
    full_name VARCHAR(40) NOT NULL 
    )""")

    cursor.execute("""
    CREATE TABLE feature_classes( 
    feature_class VARCHAR(10) PRIMARY KEY, 
    full_name VARCHAR(120) NOT NULL 
    )""")

    cursor.execute("""
    CREATE TABLE feature_codes( 
    feature_code VARCHAR(10) PRIMARY KEY, 
    full_name VARCHAR(120) NOT NULL, 
    feature_class VARCHAR(10) NOT NULL 
    )""")

    cursor.execute("""
    CREATE TABLE locations (
        geonameid INT PRIMARY KEY, 
        coordinates POINT NOT NULL
    )"""
                   )
    # cursor.execute("""
    # CREATE TABLE locations (
    #     id INT PRIMARY KEY, 
    #     full_name VARCHAR(120) NOT NULL, 
    #     latitude DOUBLE NOT NULL, 
    #     longtitude DOUBLE NOT NULL, 
    #     feature_code VARCHAR(10), 
    #     country_code VARCHAR(10) NOT NULL, 
    #     elevation INT 
    # )"""
    #                )
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

    # Defining foreign keys
    cursor.execute(""" 
    ALTER TABLE feature_codes
    ADD FOREIGN KEY (feature_class) 
    REFERENCES feature_classes(feature_class); 
    """)

    cursor.execute(""" 
    ALTER TABLE locations
    ADD FOREIGN KEY (feature_code) 
    REFERENCES feature_codes(feature_code); 
    """)
    
    cursor.execute(""" 
    ALTER TABLE locations
    ADD FOREIGN KEY (country_code) 
    REFERENCES countries(country_code); 
    """)

    cursor.execute(""" 
    ALTER TABLE reviews
    ADD FOREIGN KEY (user_id) 
    REFERENCES users(id); 
    """)

    cursor.execute(""" 
    ALTER TABLE reviews
    ADD FOREIGN KEY (place_id) 
    REFERENCES locations(id); 
    """)
    

