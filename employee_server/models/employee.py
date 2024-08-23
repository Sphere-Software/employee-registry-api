from employee_server.db import db

from sqlalchemy.orm import Mapped, mapped_column


class Employee(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)

    def __init__(
        self, id: int, first_name: str, last_name: str, email: str
    ) -> None:
        super().__init__()
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
