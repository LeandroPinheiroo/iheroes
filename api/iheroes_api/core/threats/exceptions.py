from iheroes_api.core.threats.threat import Threat


class ThreatMonitoredError(Exception):
    def __init__(self, threat: Threat):
        msg = f"threat id={threat.id} has monitored occurrence"
        super().__init__(msg)
        self.type = "threat.already_monitored_error"
        self.msg = msg

    def as_dict(self):
        return {"type": self.type, "msg": self.msg}


class ThreatNotFoundError(Exception):
    def __init__(self, msg="threat not found"):
        super().__init__(msg)
        self.type = "threat.not_found_error"
        self.msg = msg

    def as_dict(self):
        return {"type": self.type, "msg": self.msg}
