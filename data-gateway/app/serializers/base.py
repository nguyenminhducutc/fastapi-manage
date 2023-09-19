from typing import Optional, TypeVar, Generic, Union, Any
from pydantic.generics import GenericModel
from fastapi import status
from pydantic import BaseModel

T = TypeVar("T")


class BaseResponseSerialization(BaseModel):
    id: Optional[int]
    is_active: Optional[bool]


class ResponseSchemaBase(BaseModel):
    __abstract__ = True

    code: str = ''
    message: str = ''

    def custom_response(self, code: Union[str, Any], message: str):
        self.code = status.HTTP_200_OK
        self.message = message
        return self

    def success_response(self):
        self.code = status.HTTP_200_OK
        self.message = 'Thành công'
        return self


class DataResponse(GenericModel, Generic[T]):
    code: Union[int, str] = status.HTTP_200_OK
    message: Optional[str] = "Thành công"
    data: Optional[T] = None

    class Config:
        arbitrary_types_allowed = True

    async def success_response(self, data: T, code: Union[int, str] = code, message: Optional[Any] = message):
        self.code = code
        self.message = message
        self.data = data

        return self

    async def error(self, data: T = None, code: Union[int, str] = code, message: Optional[Any] = message):
        self.code = code
        self.message = message
        self.data = data
        return self


class MetadataSchema(BaseModel):
    current_page: int
    page_size: int
    total_items: int