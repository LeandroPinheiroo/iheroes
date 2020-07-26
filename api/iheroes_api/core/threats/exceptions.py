class ThreatNotFoundError(Exception):
    def __init__(self, msg="threat not found"):
        super().__init__(msg)
        self.type = "threat.not_found_error"
        self.msg = msg

    def as_dict(self):
        return {"type": self.type, "msg": self.msg}
