CREATE TABLE locations (
        id INT PRIMARY KEY, 
        name VARCHAR(120) NOT NULL, 
        coordinates POINT NOT NULL, 
        feature_code VARCHAR(5), 
        country_code CHAR(2) NOT NULL, 
        elevation INT,
        population BIGINT UNSIGNED
    )