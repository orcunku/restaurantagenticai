# Codespaces

This folder configures GitHub Codespaces with Python 3.12 and a PostgreSQL 16 + pgvector sidecar.

After the Codespace finishes creating, run:

```bash
./scripts/start-demo.sh
```

Port 8000 is forwarded automatically and labeled **Restaurant AI Demo**. The synthetic demo works with no OpenAI key.

For live OpenAI functionality, add `OPENAI_API_KEY` as a GitHub Codespaces secret and rebuild the container, or export it in the terminal before starting the app.
