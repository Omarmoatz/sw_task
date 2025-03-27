
class Messages:
    CATEGORY_NOT_FOUND = "Category not found!"
    CATEGORY_ALREADY_EXISTS = "Category already exists!"

class CategoryNotFoundException(ValueError):
    def __init__(self, message=Messages.CATEGORY_NOT_FOUND):
        super().__init__(message)

class CategoryAlreadyExistedException(ValueError):
    def __init__(self, message=Messages.CATEGORY_ALREADY_EXISTS):
        super().__init__(message)