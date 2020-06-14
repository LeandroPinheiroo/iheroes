class HeroNotUniqueError(Exception):
    def __init__(self, user_id: int, name: str, nickname: str):
        msg = "hero already exists"
        super().__init__(msg)
        self.msg = msg
        self.user_id = user_id
        self.hero_name = name
        self.hero_nickname = nickname

    def as_dict(self):
        return {
            "msg": self.msg,
            "user_id": self.user_id,
            "hero_name": self.hero_name,
            "hero_nickname": self.hero_nickname,
        }
