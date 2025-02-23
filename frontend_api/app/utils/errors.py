from flask import jsonify


class LibraryError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {"error": self.message}, self.status_code


class BookNotAvailableError(LibraryError):
    def __init__(self, book_id):
        super().__init__(f"Book with ID {book_id} is not available", 400)


class ResourceNotFoundError(LibraryError):
    def __init__(self, resource_type, resource_id):
        super().__init__(f"{resource_type} with ID {resource_id} not found", 404)


class ValidationError(LibraryError):
    def __init__(self, message):
        super().__init__(message, 400)


def handle_library_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

