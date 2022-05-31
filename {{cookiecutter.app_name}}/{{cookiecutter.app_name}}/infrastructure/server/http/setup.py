"""
Setup functions for HTTP server.
"""
from typing import Callable

from aiohttp import web
from {{cookiecutter.app_name}}.infrastructure.server.http.handlers.health import health

HEALTH = "/health"


def _setup_routes(app: web.Application):
    # Add health endpoint
    app.router.add_get(HEALTH, health)


def configure_app(app: web.Application, startup_handler: Callable):
    """Configure the web.Application."""
    app.on_startup.append(startup_handler)
    _setup_routes(app)