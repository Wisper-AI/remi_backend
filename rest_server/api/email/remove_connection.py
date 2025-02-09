from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from pypika import Query

from .tables import Connections
from lib.rest_server.auth_bearer import handler

router = APIRouter()


@router.delete("/connections/{connection_id}")
async def remove_email_connection(
    request: Request,
    connection_id: str,
    user_metadata: dict = handler,
):
    """Remove an email connection"""
    user_id = user_metadata.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user token")

    context = request.state.context

    async with context.postgres.acquire() as conn:
        # Verify connection belongs to user
        check_query = (
            Query.from_(Connections)
            .select(Connections.id)
            .where(
                (Connections.id == connection_id)
                & (Connections.user_id == user_id),
            )
        )

        connection = await conn.fetchrow(check_query.get_sql())
        if not connection:
            raise HTTPException(status_code=404, detail="Connection not found")

        # Delete connection
        delete_query = (
            Query.from_(Connections)
            .delete()
            .where(Connections.id == connection_id)
        )

        await conn.execute(delete_query.get_sql())
        return {"message": "Connection removed successfully"}
