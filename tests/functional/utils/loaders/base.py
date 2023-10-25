from abc import ABC, abstractmethod


class Loader(ABC):

    @abstractmethod
    def post_connection(self):
        pass
