def generateErrorMessage(error_number):
    if error_number == 1062:
        return "You already wrote review for such trip"
    if error_number == 1048:
        return "Incorrect query arguments"
    else:
        return f"Unknown error code:{error_number}" 