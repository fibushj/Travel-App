SET GLOBAL innodb_buffer_pool_size=268435456;

SELECT *,(((ACOS(SIN(@lat * PI() / 180) * SIN(lat * PI() / 180) 
    + COS(@lat * PI() / 180) * COS(lat * PI() / 180) 
    * COS((@lng - lng) * PI() / 180)) * 180 / PI()) 
    * 60 * 1.1515)* 1.609344) AS distance FROM location HAVING distance<=30 ORDER BY distance ASC LIMIT 0 , 20;
    
ALTER TABLE location add column lat DECIMAL( 10, 8 ) NOT NULL;
ALTER TABLE location add column lng DECIMAL( 11, 8 ) NOT NULL;
ALTER TABLE location ADD INDEX(lat);
ALTER TABLE location ADD INDEX(lng);
update location set lat=ST_X(coordinates); -- invert in elad anton
update location set lng=ST_Y(coordinates);

SET @lat = 34.65365, @lng = 69.04978;

SELECT *,(((ACOS(SIN(@lat * PI() / 180) * SIN(lat * PI() / 180) 
    + COS(@lat * PI() / 180) * COS(lat * PI() / 180) 
    * COS((@lng - lng) * PI() / 180)) * 180 / PI()) 
    * 60 * 1.1515)* 1.609344) AS distance FROM location HAVING distance<=30 ORDER BY distance ASC LIMIT 0 , 20;


-----------------------------

-- file for temporary queries while working on them from workbench
SET SQL_SAFE_UPDATES = 0;
ALTER TABLE location ADD SPATIAL INDEX(coordinates);
ALTER TABLE location add column lat DECIMAL( 10, 8 ) NOT NULL;
ALTER TABLE location add column lng DECIMAL( 11, 8 ) NOT NULL;
ALTER TABLE location ADD INDEX(lat);
ALTER TABLE location ADD INDEX(lng);
update location set lat=ST_Y(coordinates);
update location set lng=ST_X(coordinates);
select * from location where coordinates = POINT (34.65365, 69.04978);

select * from location where id='1349943';

SELECT *,
    id, (
      6371 * acos (
      cos ( radians(@lat) )
      * cos( radians( lat ) )
      * cos( radians( lng ) - radians(@lng) )
      + sin ( radians(@lat) )
      * sin( radians( lat ) )
    )
) AS distance
FROM location
HAVING distance < 30
ORDER BY distance
LIMIT 0 , 20;

SET @lat = 34.65365, @lng = 69.04978;
ALTER TABLE location ADD INDEX(lat);
ALTER TABLE location ADD INDEX(lng);
SELECT *,(((ACOS(SIN(@lat * PI() / 180) * SIN(lat * PI() / 180) 
    + COS(@lat * PI() / 180) * COS(lat * PI() / 180) 
    * COS((@lng - lng) * PI() / 180)) * 180 / PI()) 
    * 60 * 1.1515)* 1.609344) AS distance FROM location HAVING distance<=30 ORDER BY distance ASC LIMIT 0 , 20;

SELECT ST_SRID( coordinates, 4326) from location;

ALTER TABLE location MODIFY COLUMN coordinates POINT not null srid 0;
SET GLOBAL innodb_buffer_pool_size=268435456;
update location set coordinates=POINT(ST_X(coordinates), ST_Y(coordinates));
SELECT l.name, ST_X(coordinates) latitude, ST_Y(coordinates) longitude, 
(SELECT fclass.name from feature_code fcode 
JOIN feature_class fclass ON fcode.feature_class=fclass.id and fcode.id=l.feature_code) category, 
(SELECT fcode.name from feature_code fcode WHERE fcode.id=l.feature_code) subcategory,
(SELECT c.name from country c where c.id=l.country_code) country
FROM location l, country c where l.country_code=c.id and c.name = 'armenia';

SELECT location.* FROM location, country where location.country_code=country.id and country.name = 'armenia'
and feature_code='PPL';

SELECT location.* FROM location, country, feature_code, feature_class where location.country_code=country.id and country.name = 'armenia' 
and location.feature_code=feature_code.id and feature_code.feature_class=feature_class.id and feature_class.name='city, village';

-- SELECT * FROM location, country, feature_class where country.name = 'armenia' 
-- and feature_class.name='undersea';