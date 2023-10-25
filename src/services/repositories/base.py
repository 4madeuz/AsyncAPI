from abc import ABC, abstractmethod
from elastic_transport import ObjectApiResponse


class AsyncCacheStorage(ABC):
    @abstractmethod
    async def get(self, index: str, **kwargs):
        pass

    @abstractmethod
    async def set(self, index: str, value: ObjectApiResponse, **kwargs) -> None:
        pass
