from apkit.client.models import Link, WebfingerResult
from apkit.models import CryptographicKey, Multikey, Person
from apkit.server.app import SubRouter, WebfingerResource
from apkit.server.responses import ActivityResponse
from cryptography.hazmat.primitives.asymmetric import ed25519, rsa
from fastapi import Request, Response
from fastapi.responses import JSONResponse

from ..env import HOST, USER_ID, USERNAME
from .keys import load_keys

sub = SubRouter()

rsa_private_key, ed25519_private_key = load_keys(USER_ID)


def get_actor() -> Person:
    actor = Person(
        id=f"https://{HOST}/users/{USER_ID}",
        name="User",
        preferred_username=USERNAME,
        summary="Hello, world!",
        inbox=f"https://{HOST}/users/{USER_ID}/inbox",
        outbox=f"https://{HOST}/users/{USER_ID}/outbox",
        public_key=CryptographicKey(
            id=f"https://{HOST}/users/{USER_ID}#main-key",
            owner=f"https://{HOST}/users/{USER_ID}",
        ),
        manuallyApproveFollowers=False,  # type: ignore
    )
    rsa_multikey = Multikey(
        id=f"https://{HOST}/users/{USER_ID}#main-key",
        controller=f"https://{HOST}/users/{USER_ID}",
    )
    if actor.public_key:
        public_key_rsa = rsa_private_key.public_key()
        if isinstance(public_key_rsa, rsa.RSAPublicKey):
            actor.public_key.public_key = public_key_rsa

            rsa_multikey.public_key = public_key_rsa

    ed25519_multikey = Multikey(
        id=f"https://{HOST}/users/{USER_ID}#ed25519-key",
        controller=f"https://{HOST}/users/{USER_ID}",
    )
    public_key_ed25519 = ed25519_private_key.public_key()
    if isinstance(public_key_ed25519, ed25519.Ed25519PublicKey):
        ed25519_multikey.public_key = public_key_ed25519

    actor.assertion_method = [rsa_multikey, ed25519_multikey]

    return actor

@sub.webfinger()
async def webfinger_endpoint(request: Request, acct: WebfingerResource) -> Response:
    if acct.username == USERNAME and acct.host == HOST:
        link = Link(
            rel="self",
            type="application/activity+json",
            href=f"https://{HOST}/users/{USER_ID}"
        )
        wf_result = WebfingerResult(subject=acct, links=[link])
        return JSONResponse(wf_result.to_json(), media_type="application/jrd+json")
    return JSONResponse({"message": "Not Found"}, status_code=404)

@sub.get("/users/{identifier}")
async def get_actor_endpoint(identifier: str):
    if identifier == USER_ID:
        actor = get_actor()
        return ActivityResponse(actor)
    return JSONResponse({"error": "Not Found"}, status_code=404)
