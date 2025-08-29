from contextlib import ContextDecorator
from typing import Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

from dbos._dbos import DBOS


class DBOSMutex(ContextDecorator):
    def __init__(self, name: str):
        self.name = name
        self.session: Optional[Session] = None

    def __enter__(self):
        DBOS.sql_session.execute(
            text("SELECT pg_advisory_xact_lock(('x'||md5(:name))::bit(64)::bigint)"),
            {"name": self.name},
        ).fetchone()
        return self

    def __exit__(self, *exc):
        return False
