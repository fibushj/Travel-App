# import pandas
import mysql.connector

db_name = "sadna_project"

# This code creates connection to MySql, and creates new data base for project
mydb = mysql.connector.connect(
  option_files='my.conf'
)
mycursor = mydb.cursor()
mycursor.execute(f"CREATE DATABASE {db_name}")
mycursor.execute(f"USE {db_name}")
mycursor.execute("CREATE TABLE locations ( id INT PRIMARY KEY, full_name VARCHAR(120) NOT NULL, latitude DOUBLE NOT NULL, longtitude DOUBLE NOT NULL, feature_code VARCHAR(10) NOT NULL, country_code VARCHAR(10) NOT NULL, elevation INT )")
mycursor.execute("CREATE TABLE feature_codes ( feature_code VARCHAR(10) PRIMARY KEY, full_name VARCHAR(120) NOT NULL, feature_class VARCHAR(10) NOT NULL )")
mycursor.execute("CREATE TABLE feature_classes ( feature_class VARCHAR(10)  PRIMARY KEY, full_name VARCHAR(120) NOT NULL )")
mycursor.execute("CREATE TABLE countries ( country_code INT  PRIMARY KEY, full_name VARCHAR(40) NOT NULL )")
mycursor.execute("CREATE TABLE users ( id INT AUTO_INCREMENT PRIMARY KEY, full_name VARCHAR(80) NOT NULL, date_of_birth DATETIME NOT NULL )")
mycursor.execute("CREATE TABLE reviews ( user_id INT NOT NULL, place_id INT NOT NULL, rating INT NOT NULL, trip_type VARCHAR(45) , trip_season VARCHAR(45) NOT NULL, anonimous_review TINYINT, review TINYTEXT, PRIMARY KEY (user_id, place_id, trip_season))")

mydb.close()




# Purpose of this function is to take chunk of data, process it, and insert to our database
# def process_chunk(chunk):
#     for _, row in chunk.iterrows():
#         print(row[0], row[1])

# Here is the "main" loop of script, that reads data from large CSV file, by chunks. Size of chunks measured in rows, number of which we set in - "chunk_size" variable
# chunk_size = 3
# i = 0
# for chunk in pandas.read_csv("geonames.csv", chunksize=chunk_size):
    #process_chunk(chunk)
    # Code for limiting information readed
    # i += 1
    # if i > 3:
    #     break
