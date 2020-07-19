from iheroes_api.core.protocols import ThreatRepo
from iheroes_api.core.threats.threat import ReportThreatDto, Threat


async def report_threat(repo: ThreatRepo, dto: ReportThreatDto) -> Threat:
    return await repo.upsert(dto)
