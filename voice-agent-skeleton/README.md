# voice-agent-skeleton

A minimal webhook that bridges an incoming Twilio phone call to an ElevenLabs Conversational AI agent.

## What it is

A small FastAPI app with two endpoints:

- `POST /twilio/incoming-call` — Twilio hits this when a call comes in. It returns TwiML that opens a Media Stream (or `<Connect><Stream>`) toward the app.
- `POST /elevenlabs/signed-url` — issues a short-lived signed WebSocket URL for the ElevenLabs Conversational AI agent, which is what actually carries the two-way audio.

This is the connective tissue pattern behind "call a phone number, talk to an AI agent" — the part that's specific to combining Twilio telephony with ElevenLabs' voice agent, independent of whatever the agent is grounded in (a knowledge base, a RAG store, a CRM).

## When to use it

- You're wiring a phone number to a conversational voice agent and need the webhook shape Twilio and ElevenLabs expect.
- You want to see the signed-URL handshake (why you can't just hardcode the ElevenLabs agent's WebSocket URL) before building a full call-handling service.
- You're prototyping voice AI and want the minimum viable bridge before adding call recording, transfer, or multi-agent routing.

## The gotcha it solves

**The ElevenLabs agent URL is not static — it must be signed per call, or the connection is rejected.** A common first mistake is pointing Twilio's stream directly at a fixed ElevenLabs URL copied from a dashboard. That works in a demo and fails in production because:

- Signed URLs expire, so a hardcoded URL goes stale.
- Without per-call signing, you can't scope or audit which call produced which agent session.

This skeleton requests a fresh signed URL from the ElevenLabs API for every incoming call, so the connection always uses a valid, short-lived credential instead of a copy-pasted one.

## How to run

This is an **illustrative skeleton** — it defines the webhook contract, not a deployable call center.

```bash
pip install fastapi uvicorn httpx

cp .env.example .env   # fill in real keys
uvicorn main:app --reload --port 8000
```

Point a Twilio phone number's "A Call Comes In" webhook at `https://<your-tunnel>/twilio/incoming-call` (use `ngrok` or similar for local testing).

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `ELEVENLABS_API_KEY` | yes | ElevenLabs API key |
| `ELEVENLABS_AGENT_ID` | yes | ID of the Conversational AI agent to connect the call to |
| `TWILIO_AUTH_TOKEN` | yes | Used to validate that incoming webhook requests are really from Twilio |

## What's simplified here (not production-hardened)

- No Twilio request-signature validation shown beyond a stub — a real deployment must verify `X-Twilio-Signature` on every request.
- No call recording, transcription storage, or retry logic if the signed-URL request fails.
- No multi-tenant routing (one agent ID, one flow) — a real system maps phone numbers to different agents/tenants.
