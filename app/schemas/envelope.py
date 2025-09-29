# src/app/schemas/envelope.py
from typing import Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel

T = TypeVar("T")


class Envelope(BaseModel, Generic[T]):
    data: Optional[Union[T, List[T]]] = None
    detail: str
    message: str
    status_code: int
