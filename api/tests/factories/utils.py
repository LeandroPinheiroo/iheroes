def make_many(factory, amount=3, **override):
    return [factory(**override) for _ in range(amount)]
