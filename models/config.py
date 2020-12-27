with open("models/config.txt", 'r') as f:
    db_name = f.readline().strip()
    dataset_path = f.readline().strip()
    country_codes_path = f.readline().strip()
    feature_classes_path = f.readline().strip()
    feature_codes_path = f.readline().strip()