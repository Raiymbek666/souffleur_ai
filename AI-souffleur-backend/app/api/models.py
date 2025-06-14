from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class IncomingMessage(BaseModel):
    id: Optional[str] = None
    call_id: str
    from_: Literal["client", "operator"] = Field(..., alias="from")
    text: str
    time: Optional[str] = None

    model_config = {
        "validate_by_name": True
    }


class IncomingDialog(BaseModel):
    call_id: str
    messages: List[IncomingMessage]


class ClientInfo(BaseModel):
    phone: str = "string"
    name: str = "string"
    contract: str = "string"
    product: str = "string"
    loyalty: str = "string"


class MessageOut(BaseModel):
    id: str
    call_id: str
    from_: Literal["client", "operator"]
    text: str
    time: str

    model_config = {
        "populate_by_name": True
    }


class DialogResponse(BaseModel):
    call_id: str
    created_at: str
    client: ClientInfo
    messages: List[MessageOut]


class Suggestion(BaseModel):
    text: str
    type: str = "answer"
    source: str
    confidence: float


class FullResponse(BaseModel):
    status: str
    dialog: DialogResponse
    suggestions: List[Suggestion]