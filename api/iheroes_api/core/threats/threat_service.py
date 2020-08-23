from iheroes_api.core.protocols import ThreatMonitor, ThreatRepo
from iheroes_api.core.threats.threat import ReportThreatDto, Threat


async def report_threat(
    monitor: ThreatMonitor, repo: ThreatRepo, dto: ReportThreatDto
) -> Threat:
    threat: Threat = await repo.upsert(dto)

    if threat.is_being_monitored() is False:
        threat = await repo.create_pending_occurrence(threat)
        await monitor.start_monitoring(threat)

    return threat
