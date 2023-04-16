class BadRequest(Exception):
    pass


class CustomException(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


def abort(status_code=400, message="Reason not given"):
    raise CustomException(status_code, message)
