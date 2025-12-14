class ApplicationException(Exception):
    detail = "Общая ошибка приложения"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)

class ObjectNotFoundException(ApplicationException):
    detail = "Объект не найден"

class AddObjectException(ApplicationException):
   detail = "Объект уже существует"

class NoRoomsAvailableException(ApplicationException):
    detail = "Нет свободных номеров" 

class ValidationException(ApplicationException):
    detail = "Данные не корректны"