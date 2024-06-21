from typing import Optional

from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = "Something went wrong"

    def __init__(self, status_code: Optional[int] = None, detail: Optional[str] = None):
        super().__init__(
            status_code=self.status_code or status_code,
            detail=self.detail or detail
        )


class UserNotFoundException(BookingException):
    pass


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class IncorrectEmailException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта"


class IncorrectPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный пароль"


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class RoomCanNotBeBookedException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Не осталось свободных номеров'


class BookingNotFoundException(BookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Не существует бронирования с таким id'


class BookingCannotBeDeletedException(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Невозможно удалить бронирование: его не существует или нет прав'


class NotAuthorizedException(BookingException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'У вас нет прав для совершения этого действия'
