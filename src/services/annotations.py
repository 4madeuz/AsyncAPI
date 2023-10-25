import typing
from abc import ABC, abstractmethod

from fastapi import Query


class _Params(ABC):

    def __init__(self, default):
        self.default = default

    @abstractmethod
    def annotations(self):
        pass

    @abstractmethod
    def default(self):
        pass


class PageNumber(_Params):

    @classmethod
    def annotations(cls):
        return typing.Annotated[int, Query(default=1, description='Pagination page number', ge=1)]

    @classmethod
    def default(cls):
        return 1


class PageSize(_Params):

    @classmethod
    def annotations(cls):
        return typing.Annotated[int, Query(default=50, description='Pagination page size', ge=1)]

    @classmethod
    def default(cls):
        return 50
