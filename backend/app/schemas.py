from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

Importance = Literal["low", "medium", "high", "critical"]

Category = Literal[
    "public",
    "internal",
    "restricted",
    "confidential",
]


class DocumentInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    external_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    responsible_unit: str = Field(min_length=1)
    created_at: date
    url: HttpUrl
    file_type: str = Field(min_length=1)
    reading_time_minutes: int = Field(gt=0)
    importance: Importance
    category: Category
    active: bool = Field(strict=True)
