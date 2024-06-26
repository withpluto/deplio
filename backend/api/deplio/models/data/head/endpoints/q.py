from typing import Annotated, Optional
from uuid import UUID

from pydantic import AnyHttpUrl, BaseModel, Field

from ..db.enums import HTTPMethod
from ..db.q import QRequest, QResponse
from ..responses import DeplioResponse


class GetQMessagesResponse(DeplioResponse):
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
    metadata: Optional[dict[str, str]] = Field(None)


PostQMessagesRequest = Annotated[
    list[QMessage],
    Field(..., max_length=10, title='Messages'),
]


class PostQMessagesResponse(DeplioResponse):
    request_ids: list[UUID]
    messages_delivered: int
