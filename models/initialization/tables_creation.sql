CREATE TABLE country(
    id CHAR(2) PRIMARY KEY,
    name VARCHAR(58) NOT NULL
);

CREATE TABLE feature_class(
    id CHAR(1) PRIMARY KEY,
    name VARCHAR(22) NOT NULL
);

CREATE TABLE feature_code(
    id VARCHAR(5) PRIMARY KEY,
    feature_class CHAR(1) NOT NULL,
    name VARCHAR(47) NOT NULL,
    description VARCHAR(233)
);

CREATE TABLE location (
    id INT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    coordinates POINT NOT NULL,
    feature_code VARCHAR(5),
    country_code CHAR(2) NOT NULL,
    elevation INT,
    population BIGINT UNSIGNED
);

CREATE TABLE user(
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL
);

CREATE TABLE trip_type (
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(45) NOT NULL
);

CREATE TABLE trip_season(
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(45) NOT NULL
)

CREATE TABLE review(
    user_id INT NOT NULL,
    place_id INT NOT NULL,
    rating INT NOT NULL,
    trip_type INT NOT NULL,
    trip_season INT NOT NULL,
    anonymous_review TINYINT,
    review TEXT,
    PRIMARY KEY (user_id, place_id, trip_season)
);