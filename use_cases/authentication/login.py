from models.errors import InvalidCredentials


def authenticate_user(credentials) -> str:
    if credentials.email == "very" and credentials.password == "nice":
        return "token"
    raise InvalidCredentials
