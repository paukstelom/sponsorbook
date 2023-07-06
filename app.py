import logging
from typing import Any

import structlog
import uvicorn
from asgi_correlation_id import correlation_id, CorrelationIdMiddleware
from fastapi import FastAPI

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

def add_correlation(
    logger: logging.Logger, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """Add request id to log message."""
    if request_id := correlation_id.get():
        event_dict["request_id"] = request_id
    return event_dict

structlog.configure(
    processors=[
        add_correlation,
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
app.add_middleware(CorrelationIdMiddleware)

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


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=25565, reload=True)
