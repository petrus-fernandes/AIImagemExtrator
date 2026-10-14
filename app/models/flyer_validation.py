from datetime import datetime
from typing import Any

from sqlalchemy import BigInteger, DateTime, LargeBinary, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class FlyerValidation(Base):
    __tablename__ = "flyer_validation"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    image: Mapped[bytes | None] = mapped_column(LargeBinary)

    response: Mapped[str | None] = mapped_column(Text)

    reserved_by: Mapped[str | None] = mapped_column(String(255))

    reserved_date: Mapped[datetime | None] = mapped_column(DateTime)

    creation_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    def __init__(self, image, response, **kw: Any):
        super().__init__(**kw)
        self.image = image
        self.response = response
