from contextlib import contextmanager
from typing import Any, Dict, Iterable, Union

from sqlalchemy.schema import Table

from iheroes_api.infra.database.sqlalchemy import init_database, metadata

ValuesType = Dict[str, Any]


def _truncate_tables():
    metadata.bind.execute(
        """TRUNCATE {} RESTART IDENTITY""".format(
            ",".join(f'"{table.name}"' for table in reversed(metadata.sorted_tables))
        )
    )


@contextmanager
def clear_database():
    init_database()
    _truncate_tables()
    yield
    _truncate_tables()


def insert_model(model: Table, values: Union[ValuesType, Iterable[ValuesType]]) -> None:
    query = model.insert()
    if isinstance(values, Dict):
        metadata.bind.execute(query, **values)
    else:
        metadata.bind.execute(query, list(values))
