import logging
from typing import List, TypedDict

from fastapi.applications import FastAPI
from socketio import AsyncClient

from iheroes_api.api.container import Dependencies
from iheroes_api.config.environment import Env, Settings
from iheroes_api.core.threats import threat_service
from iheroes_api.core.threats.threat import ReportThreatDto

logger = logging.getLogger("SocketIO Client")


class Location(TypedDict):
    lat: float
    lng: float


class OccurrenceEvent(TypedDict):
    location: List[Location]
    dangerLevel: str  # noqa: N815
    monsterName: str  # noqa: N815


def init_sio_client(settings: Settings, deps: Dependencies, app: FastAPI) -> FastAPI:
    sio = AsyncClient()
    url = settings.LISTENER_URL

    @sio.event
    def connect():
        logger.info(f"Connected to {url}...")

    @sio.event
    def disconnect():
        logger.info("Disconnecting...")

    @sio.event
    async def occurrence(event: OccurrenceEvent):
        dto = ReportThreatDto(
            name=event["monsterName"],
            danger_level=event["dangerLevel"].lower(),
            location=event["location"][0],
        )
        threat = await threat_service.report_threat(deps.threat_repository, dto)
        logger.info(f"Reported threat of name {threat.name}")

    # App event handlers
    async def start_listener():
        if settings.ENV == Env.testing:
            return
        await sio.connect(url)

    async def stop_listener():
        await sio.disconnect()

    app.on_event("startup")(start_listener)
    app.on_event("shutdown")(stop_listener)

    return app
