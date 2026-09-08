# European AI Front Desk for Restaurants

Runnable MVP for an EU-focused restaurant guest agent across **web chat, WhatsApp and phone**, with restaurant-specific RAG, agentic reservation actions, provider adapters and a simple admin API.

## What is included

- Multi-tenant restaurants and restaurant-scoped knowledge
- PostgreSQL + pgvector semantic retrieval
- OpenAI Responses API function calling for retrieval + actions
- Reservation adapter: built-in mock + generic webhook adapter
- POS adapter interface + generic webhook menu fetch
- Twilio WhatsApp webhook
- Twilio Voice `<Gather>` speech loop
- Web chat widget
- Conversation/message/reservation persistence
- Basic AI disclosure and allergy escalation policy
- Admin endpoints for restaurant creation, knowledge ingestion and metrics
- Docker Compose local environment

## 1. Run locally

```bash
cp .env.example .env
# Put your OPENAI_API_KEY in .env
docker compose up --build
```

Open http://localhost:8000 . The database seeds `demo-bistro` automatically.

Without an OpenAI key the web UI runs in retrieval-only demo mode; agentic reservations require an OpenAI key.

## 2. Test the chat API

```bash
curl -X POST http://localhost:8000/api/chat/demo-bistro \
  -H 'content-type: application/json' \
  -d '{"message":"Habt ihr vegane Gerichte?","user_id":"demo-user"}'
```

Try: `Ich möchte Freitag um 19:30 für vier Personen reservieren. Name Anna Berger.` The mock reservation adapter always accepts parties up to 8.

## 3. Add restaurant knowledge

```bash
curl -X POST http://localhost:8000/api/admin/restaurants/demo-bistro/knowledge \
 -H 'X-Admin-Key: change-me' -H 'content-type: application/json' \
 -d '{"kind":"menu","title":"Dessert","content":"Apfelstrudel €9; enthält Gluten und Milch."}'
```

For production replace the single admin API key with SSO/RBAC and a real dashboard.

## 4. Connect Twilio WhatsApp

Expose the service using a public HTTPS domain (for local development, a secure tunnel is fine). Set your incoming WhatsApp webhook to:

`POST https://YOUR_DOMAIN/webhooks/twilio/whatsapp?restaurant=demo-bistro`

Set `TWILIO_AUTH_TOKEN` and use `APP_ENV=production` to enforce Twilio signature validation.

## 5. Connect Twilio Voice

Configure the Twilio phone number incoming Voice webhook:

`POST https://YOUR_DOMAIN/webhooks/twilio/voice/incoming?restaurant=demo-bistro`

The implementation discloses the digital assistant, uses speech `<Gather>`, sends recognized text through the same agent, speaks the answer, and loops for the next request.

For a higher-quality production voice experience, replace `<Gather>` turn-taking with a streaming/realtime voice adapter, but keep the same `run_agent`/tool layer.

## 6. Connect a reservation provider

The cleanest contract is to place a thin provider-specific bridge behind the generic webhook adapter. Configure a restaurant with:

```json
{
  "reservation_provider": "webhook",
  "reservation_config": {
    "base_url": "https://your-provider-bridge.example.com",
    "token": "secret"
  }
}
```

Your bridge implements:

### `POST /availability`
Request:
```json
{"start_at":"2026-09-11T19:30:00+02:00","party_size":4,"seating":"terrace"}
```
Response:
```json
{"available":true,"start_at":"2026-09-11T19:30:00+02:00","seating":"terrace"}
```

### `POST /reservations`
Receives guest name/contact, date/time, party size, seating and notes. Return:
```json
{"ok":true,"provider_id":"abc-123"}
```

### `POST /reservations/{provider_id}/cancel`
Return `{"ok":true,"status":"cancelled"}`.

Create dedicated adapters for aleno, TheFork, DISH, resmio, gastronovi, etc. once you have API/partner access; do not scrape their dashboards.

## 7. POS integration

`app/integrations/pos.py` defines a generic menu fetch contract. In production, normalize POS data into structured restaurant knowledge (dish, price, dietary tags, EU allergen codes, active/available status) and re-embed changed textual descriptions.

## 8. EU production checklist

This repository is an MVP, **not a legal/compliance certification**. Before real guests use it:

- Provide clear AI disclosure on voice/chat.
- Create GDPR records of processing, DPAs and subprocessor list.
- Decide whether calls are recorded; if so, obtain legally appropriate notice/consent and define retention.
- Minimize stored personal data and add deletion/export workflows.
- Treat allergy information conservatively: retrieve verified information but escalate severe-allergy safety assurances to humans.
- Add human handoff routing (SMS/Slack/POS/task queue) and business-hours behavior.
- Add audit logs for tool calls and reservation changes.
- Add idempotency keys to provider actions.
- Add rate limiting, WAF/reverse proxy, secrets management, encrypted backups, monitoring and error tracking.
- Add SSO/RBAC per restaurant/group.
- Add webhook replay protection and outbound provider retry queues.
- Pin/test model versions and regression-test critical conversations before model upgrades.

## 9. Suggested production architecture

```text
Guest
  ├─ Phone -> Twilio/voice adapter ─┐
  ├─ WhatsApp -> messaging adapter ├─> Channel API
  └─ Web widget -------------------┘
                                      |
                                  Agent service
                           ┌──────────┴──────────┐
                           |                     |
                       RAG/knowledge        Action tools
                           |              ┌──────┼───────┐
                    Postgres/pgvector  Reservations POS CRM
                                             |
                                      human escalation
```

## 10. Recommended next engineering milestones

1. Build provider-specific reservation adapter for the system used by the first pilot restaurant.
2. Replace global admin key with authenticated SaaS admin UI.
3. Structured menu/allergen schema and POS sync.
4. Streaming voice/realtime adapter and multilingual voice selection.
5. WhatsApp outbound templates/confirmation flows.
6. Human handoff inbox and notifications.
7. Background job queue for provider retries, ingestion and analytics.
8. Metrics dashboard: calls answered, after-hours calls, AI resolution rate, bookings, guests, estimated booking value, handoffs and failure rate.
9. Data retention/deletion controls and audit log.
10. Multi-location organization/billing model.

## API notes

The agent uses OpenAI's Responses API with custom function tools and `previous_response_id` for tool-result continuation. Embeddings use `text-embedding-3-small` (1536 dimensions), matching the pgvector column.

## Client-facing synthetic demo

The root URL (`/`) is now a polished, generic sales-demo environment that does **not** need real restaurant data, reservation credentials, Twilio, or an OpenAI API key.

It includes three fictional EU restaurants and synthetic:

- 30-day KPI dashboard
- phone / WhatsApp / web channel metrics
- reservations and estimated booking value
- conversation review and safe human handoffs
- restaurant-specific menu, hours, policies and allergy guardrails
- integration architecture
- interactive deterministic guest scenarios with visible agent/tool traces

Run with the normal Docker setup and visit `http://localhost:8000`.

Synthetic demo endpoints:

- `GET /demo/restaurants`
- `GET /demo/dashboard/{slug}`
- `POST /demo/chat/{slug}` with `{ "message": "..." }`

The synthetic demo is deliberately separate from the production-style `/api/chat/{slug}` route, so client presentations never depend on external providers.

## GitHub Codespaces (recommended for the client demo)

This repository includes a ready-to-use `.devcontainer` configuration. It starts a Python 3.12 development container plus PostgreSQL 16 with pgvector, so you do not need Docker Desktop on your Windows PC.

### Fastest path

1. Push this folder to a GitHub repository.
2. On GitHub, choose **Code → Codespaces → Create codespace on main**.
3. Wait for the Codespace setup to finish.
4. In the Codespace terminal run:

```bash
./scripts/start-demo.sh
```

5. Codespaces forwards port `8000` automatically. If the browser does not open, use the **Ports** tab and click **Open in Browser** next to `Restaurant AI Demo` / port `8000`.

The synthetic client demo does **not** require an OpenAI API key.

### Optional: enable live OpenAI agent features

Add `OPENAI_API_KEY` as a Codespaces secret in GitHub, then rebuild/recreate the Codespace. The `.devcontainer` passes the secret into the workspace when present.

### Useful commands

```bash
./scripts/start-demo.sh          # start the demo
pytest                           # run tests
ruff check app tests             # lint Python
```

To stop the app, press `Ctrl+C` in the terminal. The PostgreSQL/pgvector service is managed automatically by the Codespace.
