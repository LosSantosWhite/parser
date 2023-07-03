import datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger
from app.database.postgresql.base import Base


class Auction(Base):
    __tablename__ = "auction"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date]
    location: Mapped[str]
    region: Mapped[Optional[str]]
    status: Mapped[str]
    deadline: Mapped[Optional[datetime.date]]
    fee: Mapped[Optional[int]] = mapped_column(BigInteger)
    organizer: Mapped[str]
    obj_id: Mapped[str]

    def __repr__(self):
        return f"<Autcion(id={self.id}, location={self.location}, region={self.region}, status={self.status})>"
