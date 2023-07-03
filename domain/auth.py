from models.user_models import User


class SessionEncoder:
    def encode(self, user: User) -> str:
        ...
