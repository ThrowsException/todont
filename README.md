# TODONT

This is the worlds most complicated to do app built entirely by agents

## Features
- Todo App with Oauth login
- CRDT Real time collaboration
- Full Developer Portal
- Event Based Architecture
- LLM Supported Assisstant
- Scheduling and Reminders
- CQRS Micro Services
- Shared workspaces
- Social Media Integration
- Gamification
- Exports/Backups
- Completely Opensource and self hosted
- API with llm.txts, MCP, and OpenAPI Swagger

## Goals
Given a relatively easy "hello world" program that most developers would build in a few hours to learn some new technology, how bizarrely complicated can we make it given that the human brain is no longer the thing that is being used and just burn tokens to build wild s***. 

## Development
Whatever the AI's deem necessary

## Plan
* Create 4 Agents, Frontend, Backend, Architect, QA, Devops, Cost, Monitor
* Agents must work together to build a deployable production grade system
* Cost must be as close to 0 as possible


## Resources
https://www.canirun.ai/

## Running

### Local setup
```bash
bin/bootstrap        # starts DynamoDB Local + Keycloak, creates table + realm/client
source bin/test_env  # sets AWS_ENDPOINT_URL_DYNAMODB, KEYCLOAK_* env vars
```

### Backend
```bash
uv run fastapi dev app/main.py
```

### Getting a token
```bash
TOKEN=$(curl -s -X POST "$KEYCLOAK_URL/realms/$KEYCLOAK_REALM/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=$KEYCLOAK_CLIENT_ID&client_secret=$KEYCLOAK_CLIENT_SECRET" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/todos
```

### Linting
```bash
uv run ruff check app/ tests/
uv run ruff check --fix app/ tests/
```

### Testing
```bash
uv run pytest -v
```

### Docker
Should be possible with any model but locally im using this currently

`docker model run ai/llama3.1`
`docker sandbox run opencode ~/projects/complicated_todo`

## Useful commands
`opencode session list | grep 'ses' | awk '{ print $1 }' | xargs -I {} opencode session delete {}`