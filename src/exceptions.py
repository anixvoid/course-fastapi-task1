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

class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"

class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"

class UserNotFoundException(ObjectNotFoundException):
    detail = "Пользователь с таким email не зарегистрирован"

class ObjectAlreadyExistsException(ApplicationException):
    detail = "Похожий объект уже существует"

class UserAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Пользователь с такой почтой уже существует"

class AddObjectException(ApplicationException):
   detail = "Ошибка при добавлении объекта"

class NoRoomsAvailableException(ApplicationException):
    detail = "Нет свободных номеров" 

class ValidationException(ApplicationException):
    detail = "Данные не корректны"

class UserAlreadyExistsHTTPException(ApplicationHTTPException):
    status_code = 409
    detail = "Пользователь с такой почтой уже существует"

class HotelNotFoundHTTPException(ApplicationHTTPException):
    status_code = 404
    detail = "Отель не найден"

class RoomNotFoundHTTPException(ApplicationHTTPException):
    status_code = 404
    detail = "Номер не найден"

class IncorrectAccessTokenException(ApplicationException):
    detail="Не верный токен доступа"

class ExpiredAccessTokenException(ApplicationException):
    detail="Истек срок действия токена доступа"

class IncorrectAccessTokenHTTPException(ApplicationHTTPException):
    status_code = 401
    detail="Не верный токен доступа"

class ExpiredAccessTokenHTTPException(ApplicationHTTPException):
    status_code = 401
    detail="Истек срок действия токена доступа"

class IncorrectPasswordExpcetion(ApplicationException):
    detail = "Пароль не верный"

class IncorrectPasswordHTTPExpcetion(ApplicationHTTPException):
    status_code = 401
    detail = "Пароль не верный"    

class UserNotFoundHTTPException(ApplicationHTTPException):
    status_code = 401
    detail = "Пользователь с таким email не зарегистрирован"