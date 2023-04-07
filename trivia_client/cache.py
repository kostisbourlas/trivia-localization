import abc
from typing import Optional


class AbstractCache(abc.ABC):
    @abc.abstractmethod
    def get(self, key: str):
        pass

    @abc.abstractmethod
    def set(self, key: str, value: str):
        pass


class DictCache(AbstractCache):
    """
    Attributes:
        _cache_dict (dict): A Python Dictionary used as poor man's cache.
    """

    def __init__(self):
        self._cache_dict = dict()

    def get(self, key: str) -> Optional[str]:
        return self._cache_dict.get(key, None)

    def set(self, key: str, value: str) -> None:
        self._cache_dict[key] = value
