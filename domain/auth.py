from models.user_models import User


class EncodeSession:
    def __call__(self, user: User) -> str:
        ...


class HashPassword:
    def __call__(self, password: str) -> str:
        ...


class VerifyPassword:
    def __call__(self, password: str, user: User) -> bool:
        ...
