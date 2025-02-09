from datetime import datetime
from typing import List
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic import EmailStr


class EmailConnectionCreate(BaseModel):
    """Request model for creating a new email connection"""

    provider_id: str
    email_address: EmailStr
    access_token: str
    refresh_token: Optional[str] = None
    token_expires_at: Optional[datetime] = None
    scopes: Optional[List[str]] = None


class EmailConnectionResponse(BaseModel):
    """Response model for email connection details"""

    id: UUID
    email_address: str
    provider_id: str
    created_at: datetime
    is_active: bool = True


class EmailConnectionList(BaseModel):
    """Response model for listing email connections"""

    connections: List[EmailConnectionResponse]
