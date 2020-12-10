def populate_tables(cursor):
    cursor.execute("""
    LOAD DATA INFILE 'd:\Jonathan\Software\Projects\DB-Project\data\small.csv'
    INTO TABLE sadna_project.locations
    FIELDS TERMINATED BY ',' ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS
    (id, latitude);
    """
    )



# Purpose of this function is to take chunk of data, process it, and insert to our database
# def process_chunk(chunk):
#     for _, row in chunk.iterrows():
#         print(row[0], row[1])

# Here is the "main" loop of script, that reads data from large CSV file, by chunks. Size of chunks measured in rows, number of which we set in - "chunk_size" variable
# chunk_size = 3
# i = 0
# for chunk in pandas.read_csv("geonames.csv", chunksize=chunk_size):
# process_chunk(chunk)
# Code for limiting information readed
# i += 1
# if i > 3:
#     break