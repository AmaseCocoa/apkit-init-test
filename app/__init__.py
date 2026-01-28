from apkit.server.app import ActivityPubServer

from . import actor, nodeinfo

app = ActivityPubServer()
app.inbox("/users/{identifier}/inbox")
app.outbox("/users/{identifier}/outbox")  

app.include_router(actor.sub)
app.include_router(nodeinfo.sub)