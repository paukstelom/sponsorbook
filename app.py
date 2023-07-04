import logging

import structlog
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from routers import (
    sponsors,
    tickets,
    events,
    sub_organizations,
    organizations,
    categories,
    contacts,
    users,
    conversations,
    authentication,
    imports,
)

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.render_to_log_kwargs,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


app.include_router(sponsors.router)
app.include_router(tickets.router)
app.include_router(events.router)
app.include_router(sub_organizations.router)
app.include_router(organizations.router)
app.include_router(categories.router)
app.include_router(contacts.router)
app.include_router(users.router)
app.include_router(conversations.router)
app.include_router(authentication.router)
app.include_router(imports.router)
