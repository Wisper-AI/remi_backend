from uuid import UUID

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from pypika import Order
from pypika import Query

from .schema import EmailConnectionList
from .schema import EmailConnectionResponse
from .tables import Connections
from lib.rest_server.auth_bearer import handler

router = APIRouter()


@router.get("/connections", response_model=EmailConnectionList)
async def list_email_connections(
    request: Request,
    user_metadata: dict = handler,
):
    """List all email connections for the user"""
    user_id = user_metadata.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user token")

    context = request.state.context

    async with context.postgres.acquire() as conn:
        query = (
            Query.from_(Connections)
            .select(
                Connections.id,
                Connections.email_address,
                Connections.provider_id,
                Connections.created_at,
                Connections.is_active,
            )
            .where(Connections.user_id == user_id)
            .orderby(Connections.created_at, order=Order.desc)
        )

        connections = await conn.fetch(query.get_sql())

        return EmailConnectionList(
            connections=[
                EmailConnectionResponse(
                    id=UUID(row["id"]),
                    email_address=str(row["email_address"]),
                    provider_id=str(row["provider_id"]),
                    created_at=row["created_at"],
                    is_active=row["is_active"],
                )
                for row in connections
            ],
        )
