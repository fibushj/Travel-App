def generateErrorMessage(error_number):
    if error_number == 1062:
        return "You already wrote review for such trip"
    else:
        return f"Unknown error code:{error_number}" 