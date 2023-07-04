class SponsorNotFound(BaseException):
    pass


class CategoryNotFound(BaseException):
    pass


class TicketNotFound(BaseException):
    pass


class EventNotFound(BaseException):
    pass


class ConversationNotFound(BaseException):
    pass


class InvalidCredentials(BaseException):
    pass


class OrganizationNotFound(BaseException):
    pass


class SubOrganizationNotFound(BaseException):
    pass


class UserNotFound(BaseException):
    pass


class CouldNotSave(BaseException):
    ...


class CouldNotInsert(BaseException):
    ...
