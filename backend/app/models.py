from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    external_id: Mapped[str] = mapped_column(String, unique=True)

    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    responsible_unit: Mapped[str] = mapped_column(String)
    created_at: Mapped[date] = mapped_column(Date)
    url: Mapped[str] = mapped_column(Text)
    file_type: Mapped[str] = mapped_column(String)
    reading_time_minutes: Mapped[int] = mapped_column(Integer)
    importance: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    active: Mapped[bool] = mapped_column(Boolean)

    imported_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.current_timestamp(),
    )
