from uuid import UUID

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from pypika import Query

from .schema import EmailConnectionCreate
from .schema import EmailConnectionResponse
from .tables import Connections
from lib.rest_server.auth_bearer import handler

router = APIRouter()


@router.post("/connections", response_model=EmailConnectionResponse)
async def add_email_connection(
    request: Request,
    connection: EmailConnectionCreate,
    user_metadata: dict = handler,
):
    """Add a new email connection for the user"""
    user_id = user_metadata.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user token")

    context = request.state.context

    # Check if connection already exists
    async with context.postgres.acquire() as conn:
        check_query = (
            Query.from_(Connections)
            .select(Connections.id)
            .where(
                (Connections.user_id == user_id)
                & (Connections.email_address == connection.email_address),
            )
        )

        existing = await conn.fetchrow(check_query.get_sql())
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Email address already connected",
            )

        # Create new connection
        insert_query = (
            Query.into(Connections)
            .columns(
                Connections.user_id,
                Connections.provider_id,
                Connections.email_address,
                Connections.access_token,
                Connections.refresh_token,
                Connections.token_expires_at,
                Connections.scopes,
            )
            .insert(
                user_id,
                connection.provider_id,
                connection.email_address,
                connection.access_token,
                connection.refresh_token,
                connection.token_expires_at,
                connection.scopes,
            )
            .returning(
                Connections.id,
                Connections.email_address,
                Connections.provider_id,
                Connections.created_at,
                Connections.is_active,
            )
        )

        result = await conn.fetchrow(insert_query.get_sql())
        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to create connection",
            )

        return EmailConnectionResponse(
            id=UUID(result["id"]),
            email_address=str(result["email_address"]),
            provider_id=str(result["provider_id"]),
            created_at=result["created_at"],
            is_active=result["is_active"],
        )
