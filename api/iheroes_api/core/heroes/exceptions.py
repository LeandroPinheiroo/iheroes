class HeroNotUniqueError(Exception):
    def __init__(self, msg="hero already exists"):
        super().__init__(msg)
        self.msg = msg
        self.type = "conflict_error.not_unique"

    def as_dict(self):
        return {"msg": self.msg, "type": self.type}
