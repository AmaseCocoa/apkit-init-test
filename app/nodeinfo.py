from apkit.nodeinfo.builder import NodeinfoBuilder
from apkit.server.app import SubRouter
from apkit.server.responses import ActivityResponse

from .env import SOFTWARE

sub = SubRouter()

@sub.nodeinfo("/nodeinfo/2.0", "2.0")
async def nodeinfo_endpoint_v2():
    builder = NodeinfoBuilder(version="2.0")
    nodeinfo = (
        builder
        .set_software(
            name=SOFTWARE,
            version="1.2.3",
            repository=None,
            homepage=None,
        )
        .set_protocols(["activitypub"])
        .set_services(inbound=[], outbound=[])
        .set_usage(
            users_total=1,
            active_halfyear=0,
            active_month=0,
            local_posts=0,
            local_comments=0,
        )
        .set_open_registrations(False)
        .set_metadata({"nodeName": SOFTWARE})
        .build()
    )
    return ActivityResponse(nodeinfo)


@sub.nodeinfo("/nodeinfo/2.1", "2.1")
async def nodeinfo_endpoint():
    builder = NodeinfoBuilder(version="2.1")
    nodeinfo = (
        builder
        .set_software(
            name=SOFTWARE,
            version="1.2.3",
            repository=None,
            homepage=None,
        )
        .set_protocols(["activitypub"])
        .set_services(inbound=[], outbound=[])
        .set_usage(
            users_total=1,
            active_halfyear=0,
            active_month=0,
            local_posts=0,
            local_comments=0,
        )
        .set_open_registrations(False)
        .set_metadata({"nodeName": SOFTWARE})
        .build()
    )
    return ActivityResponse(nodeinfo)
