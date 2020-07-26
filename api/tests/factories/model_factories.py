from functools import partial
from typing import Any, Dict, Iterable, Union

from sqlalchemy.schema import Table

from iheroes_api.infra.database.models import Hero, Threat, ThreatRecord, User
from iheroes_api.infra.database.sqlalchemy import metadata

ValuesType = Dict[str, Any]


def insert_model(model: Table, values: Union[ValuesType, Iterable[ValuesType]]) -> None:
    query = model.insert()
    if isinstance(values, Dict):
        metadata.bind.execute(query, **values)
    else:
        metadata.bind.execute(query, list(values))


insert_hero = partial(insert_model, Hero)
insert_user = partial(insert_model, User)
insert_threat = partial(insert_model, Threat)
insert_threat_record = partial(insert_model, ThreatRecord)
