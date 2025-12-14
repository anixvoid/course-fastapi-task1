from fastapi import HTTPException


class ApplicationException(Exception):
    detail = "Общая ошибка приложения"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)

class ApplicationHTTPException(HTTPException):
    status_code = 500
    detail = None
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class ObjectNotFoundException(ApplicationException):
    detail = "Объект не найден"

class ObjectAlreadyExistsException(ApplicationException):
    detail = "Похожий объект уже существует"

class AddObjectException(ApplicationException):
   detail = "Ошибка при добавлении объекта"

class NoRoomsAvailableException(ApplicationException):
    detail = "Нет свободных номеров" 

class ValidationException(ApplicationException):
    detail = "Данные не корректны"

class HotelNotFoundHTTPException(ApplicationHTTPException):
    status_code = 404
    detail = "Отель не найден"

class RoomNotFoundHTTPException(ApplicationHTTPException):
    status_code = 404
    detail = "Номер не найден"