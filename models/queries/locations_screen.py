def select():
    return """
            SELECT 
                l.name,
                lat latitude,
                lng longitude,
                (SELECT 
                        fclass.name
                    FROM
                        feature_code fcode
                            JOIN
                        feature_class fclass ON fcode.feature_class = fclass.id
                    WHERE
                        fcode.id = l.feature_code) category,
                (SELECT 
                        fcode.name
                    FROM
                        feature_code fcode
                    WHERE
                        fcode.id = l.feature_code) subcategory,
                c.name as country
            """


def from_country():
    return """
            FROM
                location l
                    JOIN
                country c ON l.country_code = c.id
            """



def where_radius():
    return """
            WHERE
            lat between @lat_min and @lat_max and lng between @lng_min and @lng_max 
            and (((ACOS(SIN(@lat * PI() / 180) * SIN(lat * PI() / 180) + COS(@lat * PI() / 180) * COS(lat * PI() / 180) * COS((@lng - lng) * PI() / 180)) * 180 / PI()) * 60 * 1.1515) * 1.609344) < @R
            """
            
def geospatial_preprocessing(radius, lat, lng):
    return f""" 
            SET @R={radius};
            SET @earth_radius = 6378;
            SET @lat = {lat};
            SET @lng = {lng};
            SET @km_per_lat_degree = @earth_radius * PI() / 180;
            SET @lat_delta = @R /@km_per_lat_degree;
            SET @lng_delta = @lat_delta / COS(@lat * PI() / 180);
            SET @lat_min = @lat - @lat_delta;
            SET @lat_max = @lat + @lat_delta;
            SET @lng_min = @lng - @lng_delta;
            SET @lng_max = @lng + @lng_delta;
    """
