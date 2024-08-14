from employee_server.db import db

from sqlalchemy.orm import Mapped, mapped_column


class Team(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    def __init__(self, name: str):
        super().__init__()
        self.name = name
