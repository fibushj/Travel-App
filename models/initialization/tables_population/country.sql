LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/ISO 3166.csv'
INTO TABLE Country
FIELDS TERMINATED BY ','
enclosed by '"'
LINES TERMINATED BY '\r\n' 
IGNORE 1 LINES
(code, name)
