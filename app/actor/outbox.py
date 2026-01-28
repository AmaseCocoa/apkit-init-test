from apkit.server.app import Context, JSONResponse, SubRouter
from apkit.types import Outbox

from ..env import USER_ID

sub = SubRouter()

@sub.on(Outbox)
async def outbox(ctx: Context):
    identifier = ctx.request.path_params.get("identifier")
    start = ctx.request.query_params.get("start", None)
    if identifier == USER_ID:
        return
    return JSONResponse({"error": "Not Found"})