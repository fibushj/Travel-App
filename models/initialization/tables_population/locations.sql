LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/small.csv' 
INTO TABLE sadna.locations
-- CHARACTER SET latin1
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 
IGNORE 1 LINES
(geonameid,@dummy,@asciiname,@dummy,@latitude,@longitude,@dummy,@feature_code,@country_code,@dummy,@admin1,@admin2,@admin3,@admin4,@population,@elevation,@dummy,@dummy,@dummy);
-- set coordinates=POINT(@latitude, @longitude);