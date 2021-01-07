select_locations = f"""
SELECT 
    l.name,
    ST_X(coordinates) latitude,
    ST_Y(coordinates) longitude,
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
