"""
Setup app and start server.
"""
import asyncio
import json
import signal
import sys
from typing import Mapping

import click
from aiohttp import ClientSession, http, web
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from {{cookiecutter.app_name}}.infrastructure.server import http


def on_startup(conf: Mapping):
    async def startup_handler(app):

        # Client Session for app, save to app
        app["PERSISSTENT_SESSION"] = ClientSession()

        app["HOST"] = conf["host"]
        app["PORT"] = conf["port"]

        async def cleanup(app):
            """Perform required cleanup on shutdown"""
            await app["PERSISSTENT_SESSION"].close()

        app.on_shutdown.append(cleanup)
    return startup_handler


@click.command()
@click.option(
    "-c",
    "--config",
    type=click.File("r"),
    default="config.json",
    help="Configuration file.",
)
def main(config):
    conf = json.load(config)
    app = web.Application()

    http.configure_app(app, on_startup(conf))

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGTERM, loop.stop)

    # Set up scheduler for cron jobs
    scheduler = AsyncIOScheduler({"apscheduler.timezone": "UTC"}, daemon=True)

    # Start the HTTP server.
    web.run_app(app)


if __name__ == "__main__":
    sys.exit(main())
