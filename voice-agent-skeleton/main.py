"""
main.py — illustrative skeleton: Twilio call -> ElevenLabs Conversational AI bridge.

Not production-hardened. No signature validation beyond a stub, no call
recording, single agent/tenant only. See README.md for what a real
deployment adds on top of this.
"""

import os

import httpx
from fastapi import FastAPI, Request, Response

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
ELEVENLABS_AGENT_ID = os.environ.get("ELEVENLABS_AGENT_ID", "")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")

ELEVENLABS_SIGNED_URL_ENDPOINT = "https://api.elevenlabs.io/v1/convai/conversation/get-signed-url"

app = FastAPI(title="voice-agent-skeleton")


def is_valid_twilio_request(request: Request) -> bool:
    """
    Stub for Twilio request-signature validation.
    A real deployment MUST verify the `X-Twilio-Signature` header using
    `twilio.request_validator.RequestValidator(TWILIO_AUTH_TOKEN)` against
    the full request URL and POST body. Skipped here to keep the skeleton
    dependency-free; do not ship this stub as-is.
    """
    return bool(TWILIO_AUTH_TOKEN)


async def get_elevenlabs_signed_url() -> str:
    """
    Request a fresh, short-lived signed WebSocket URL for the configured
    agent. Signed URLs expire — never cache or hardcode this value.
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            ELEVENLABS_SIGNED_URL_ENDPOINT,
            params={"agent_id": ELEVENLABS_AGENT_ID},
            headers={"xi-api-key": ELEVENLABS_API_KEY},
        )
        response.raise_for_status()
        return response.json()["signed_url"]


@app.post("/twilio/incoming-call")
async def incoming_call(request: Request) -> Response:
    """Twilio webhook: return TwiML that streams the call to our media handler."""
    if not is_valid_twilio_request(request):
        return Response(status_code=403, content="Invalid Twilio signature")

    host = request.headers.get("host", "localhost")
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Connect>
    <Stream url="wss://{host}/media-stream" />
  </Connect>
</Response>"""
    return Response(content=twiml, media_type="application/xml")


@app.post("/elevenlabs/signed-url")
async def signed_url() -> dict:
    """Issue a fresh signed URL for the ElevenLabs Conversational AI agent."""
    url = await get_elevenlabs_signed_url()
    return {"signed_url": url}


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
