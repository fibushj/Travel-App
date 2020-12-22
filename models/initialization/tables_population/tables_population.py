dataset_path = 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/small.csv'

def populate_tables(cursor):
    cursor.execute(f"""
    LOAD DATA INFILE {dataset_path} 
    INTO TABLE sadna.locations
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n' 
    IGNORE 1 LINES
    (@geonameid,@dummy,@asciiname,@dummy,@latitude,@longitude,@dummy,feature_code,country_code,@dummy,@dummy,@dummy,@dummy,@dummy,population,elevation,@dummy,@dummy,@dummy);
    set id=@geonameid, name=@asciiname, coordinates=POINT(@latitude, @longitude);
    """
    )
