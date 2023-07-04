from abc import ABC, abstractmethod

from models.user_models import User


class EncodeSession(ABC):
    @abstractmethod
    def __call__(self, user: User) -> str:
        ...


class HashPassword(ABC):
    @abstractmethod
    def __call__(self, password: str) -> str:
        ...


class VerifyPassword(ABC):
    @abstractmethod
    def __call__(self, password: str, user: User) -> bool:
        ...
