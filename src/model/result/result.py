from typing import TypeVar, Generic, Callable

T = TypeVar('T')


class Result(Generic[T]):
    _data: T = None
    _exception: BaseException = None

    def is_success(self) -> bool:
        """
        :return: True if this is an instance of Success
        """
        return isinstance(self, Success)

    def is_error(self) -> bool:
        """
        :return: True if this is an instance of Error
        """
        return isinstance(self, Error)

    def on_success(self, job: Callable[[T], any]):
        """
        :param job: a lambda indicates success state, passing a data T into as parameter
        """
        if self.is_success():
            job(self._data)

    def on_error(self, job: Callable[[BaseException, T], any]):
        """
        :param job: a lambda indicates error state, passing 'BaseException' and data 'T' as params
        """
        if self.is_error():
            job(self._exception, self._data)


class Success(Result):

    def __init__(self, data: T):
        self._data = data


class Error(Result):

    def __init__(self, exception: BaseException, data: T = None):
        self._data = data
        self._exception = exception
