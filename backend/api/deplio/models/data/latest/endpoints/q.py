from typing import Annotated, Optional
from uuid import UUID
from pydantic import AnyHttpUrl, BaseModel, Field
from deplio.models.data.latest.db.enums import HTTPMethod
from deplio.models.data.latest.db.q import QRequest, QResponse


class GetQMessagesResponse(BaseModel):
    class QRequestWithResponses(QRequest):
        responses: list[QResponse]

    requests: list[QRequestWithResponses]
    count: int
    total: int
    page: int
    page_size: int


class QMessage(BaseModel):
    destination: AnyHttpUrl
    body: Optional[str] = Field(None)
    method: HTTPMethod
    headers: Optional[dict[str, str]] = Field(None)


PostQMessagesRequest = QMessage | Annotated[list[QMessage], Field(..., max_length=10)]


class PostQMessagesResponse(BaseModel):
    request_ids: list[UUID]
    messages_delivered: int
