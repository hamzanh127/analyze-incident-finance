# Finance Incident Multi-Agent

[![API Tests](https://github.com/hamzanh127/analyze-incident-finance/actions/workflows/api-tests.yml/badge.svg)](https://github.com/hamzanh127/analyze-incident-finance/actions/workflows/api-tests.yml)
[![AI Agent Tests](https://github.com/hamzanh127/analyze-incident-finance/actions/workflows/agent-tests.yml/badge.svg)](https://github.com/hamzanh127/analyze-incident-finance/actions/workflows/agent-tests.yml)
[![LangGraph Workflow Tests](https://github.com/hamzanh127/analyze-incident-finance/actions/workflows/langgraph-tests.yml/badge.svg)](https://github.com/hamzanh127/analyze-incident-finance/actions/workflows/langgraph-tests.yml)
[![AI Monitoring Tests](https://github.com/hamzanh127/analyze-incident-finance/actions/workflows/monitoring-tests.yml/badge.svg)](https://github.com/hamzanh127/analyze-incident-finance/actions/workflows/monitoring-tests.yml)
[![Governance Tests](https://github.com/hamzanh127/analyze-incident-finance/actions/workflows/governance-tests.yml/badge.svg)](https://github.com/hamzanh127/analyze-incident-finance/actions/workflows/governance-tests.yml)
[![Coverage Report](https://github.com/hamzanh127/analyze-incident-finance/actions/workflows/coverage.yml/badge.svg)](https://github.com/hamzanh127/analyze-incident-finance/actions/workflows/coverage.yml)
[![Docker Build](https://github.com/hamzanh127/analyze-incident-finance/actions/workflows/docker-build.yml/badge.svg)](https://github.com/hamzanh127/analyze-incident-finance/actions/workflows/docker-build.yml)
[![Security Scan](https://github.com/hamzanh127/analyze-incident-finance/actions/workflows/security.yml/badge.svg)](https://github.com/hamzanh127/analyze-incident-finance/actions/workflows/security.yml)
[![Render Health Check](https://github.com/hamzanh127/analyze-incident-finance/actions/workflows/render-health.yml/badge.svg)](https://github.com/hamzanh127/analyze-incident-finance/actions/workflows/render-health.yml)

## Contexte Finance

`finance-incident-multi-agent` est un projet de formation backend Python conÃ§u pour analyser des incidents financiers: virements suspects, transactions inhabituelles, nouveaux bÃ©nÃ©ficiaires, risques de fraude, contraintes AML/KYC et besoin de revue humaine.

Le projet illustre une architecture professionnelle avec FastAPI, Pydantic, LangGraph, agents IA spÃ©cialisÃ©s, monitoring IA, observabilitÃ© et tests automatisÃ©s.

## Objectif

L'objectif est de fournir une API capable de recevoir un incident financier, d'orchestrer plusieurs agents spÃ©cialisÃ©s, puis de retourner une dÃ©cision structurÃ©e:

- `approved`
- `manual_review`
- `blocked`

Chaque analyse retourne aussi un `correlation_id`, des recommandations, un bloc de monitoring et un rapport final.

## Architecture Multi-Agent

L'orchestration est gÃ©rÃ©e par LangGraph.

Pipeline:

```text
START
-> risk_node
-> fraud_node
-> compliance_node
-> ai_safety_node
-> decision_node
-> monitoring_node
-> report_node
-> END
```

`SupervisorAgent` ne lance pas directement les agents. Il gÃ©nÃ¨re un `correlation_id`, crÃ©e l'Ã©tat initial, appelle le graph LangGraph compilÃ©, puis formate la rÃ©ponse finale compatible avec `AnalyzeResponse`.

## RÃ´le Des Agents

- `SupervisorAgent`: orchestre l'analyse via LangGraph et prÃ©pare la rÃ©ponse API.
- `RiskAgent`: analyse le niveau de risque financier avec Grok.
- `FraudAgent`: dÃ©tecte les signaux de fraude financiÃ¨re avec Grok.
- `ComplianceAgent`: Ã©value AML, KYC, gouvernance et besoin d'escalade conformitÃ© avec Grok.
- `MonitoringAgent`: suit l'exÃ©cution, le statut, la latence et les indicateurs d'observabilitÃ©.

## Monitoring IA

Le service inclut des contrÃ´les IA simples, dÃ©terministes et testables:

- toxicitÃ©
- hallucination
- prompt injection
- PII
- estimation de tokens
- estimation de coÃ»t
- latence

Ces contrÃ´les sont centralisÃ©s dans `app/monitoring`.

## ObservabilitÃ© Et Correlation ID

Chaque analyse retourne un identifiant de corrÃ©lation:

```text
FIN-YYYYMMDD-XXXXXX
```

Exemple:

```json
{
  "correlation_id": "FIN-20260626-ABC123"
}
```

Ce `correlation_id` permet de relier une rÃ©ponse API, un log, un Ã©vÃ©nement d'observabilitÃ© et une investigation manuelle.

## AI Observability

Le projet combine cinq niveaux d'observabilite IA:

- `MonitoringAgent`: produit le statut d'execution, la latence, les flags de monitoring local et le bloc LangSmith dans la reponse.
- `LangSmith`: trace le workflow LangGraph complet avec le run `finance_incident_analysis` et des etapes distinctes pour les agents.
- `Correlation ID`: relie la reponse API, les logs, les metriques, le rapport et les traces LangSmith.
- `Metrics`: expose les compteurs et latences via `/metrics`.
- `Logs`: conserve des evenements structures sans secrets ni donnees sensibles inutiles.

Difference importante:

- `MonitoringAgent` fait partie du workflow applicatif. Il resume l'etat d'execution et les controles locaux retournes au client.
- `LangSmith` est une plateforme externe d'observabilite. Elle observe les runs, les timings, les metadata et les etapes LangGraph, mais ne participe pas a la logique metier et ne change aucune decision.

Quand LangSmith est active, chaque trace contient notamment `correlation_id`, `request_id`, `incident_type`, `risk_level`, `decision`, `execution_time`, `environment` et `application_version`.

## Endpoints API

| MÃ©thode | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Statut du service |
| `GET` | `/health` | SantÃ© du service et des agents |
| `GET` | `/metrics` | MÃ©triques en mÃ©moire |
| `GET` | `/observability` | Configuration d'observabilite LangSmith |
| `POST` | `/analyze` | Analyse d'un incident financier |
| `POST` | `/chat` | Chat IA contextuel avec Grok, incident, resultat d'analyse et historique |

## Frontend Supervision Platform

Le frontend React + Vite est maintenant une plateforme de supervision dediee au systeme Multi-Agent Finance. Il ne modifie pas la logique backend; il consomme les endpoints FastAPI et expose les signaux du workflow.

Pages principales:

- `Dashboard`: statut global Backend, LangGraph, Grok, LangSmith, Monitoring, Docker et Render.
- `Incident Analysis`: formulaire d'incident, animation Supervisor started, progression Risk/Fraud/Compliance/Monitoring/Report et synthese de decision.
- `AI Agent Chat`: assistant IA connecte a `POST /chat`; le backend appelle Grok avec `incident`, `analysis_result` et `history`.
- `Monitoring`: centre securite avec Static Checks, Grok AI Safety Review, Telemetry et Final Security Decision.
- `LangGraph`: vue animee du workflow Supervisor -> Risk -> Fraud -> Compliance -> Monitoring -> Report.
- `Observability`: correlation ID, execution time, logs, metrics, LangSmith status, project, tracing, version et environment.

Le frontend utilise `lucide-react` pour les icones et `VITE_API_BASE_URL` pour cibler le backend:

```text
VITE_API_BASE_URL=http://localhost:8002
```

Lancement frontend:

```bash
cd frontend
npm install
npm run dev
```

Interface locale:

```text
http://localhost:5173
```

## Exemple JSON Input

```json
{
  "customer_id": "cust_123",
  "incident_type": "wire_transfer",
  "amount": 12500.0,
  "currency": "USD",
  "country": "US",
  "device": "mobile",
  "beneficiary_status": "new",
  "description": "Customer reports an unauthorized transfer to a new beneficiary."
}
```

## Exemple JSON Output

```json
{
  "correlation_id": "FIN-20260626-ABC123",
  "risk_level": "high",
  "risk_score": 90,
  "fraud_suspicion": true,
  "fraud_score": 85,
  "compliance_status": "escalation_required",
  "decision": "blocked",
  "recommendations": [
    "Review high-risk financial exposure before approval.",
    "Investigate fraud signals and verify transaction legitimacy."
  ],
  "monitoring": {
    "status": "processed",
    "execution_time_ms": 120.0
  },
  "report": {
    "summary": "Finance incident analysis completed with decision: blocked.",
    "risk_analysis": {},
    "fraud_analysis": {},
    "compliance_analysis": {},
    "ai_safety": {},
    "recommended_next_steps": [],
    "final_status": "completed"
  }
}
```

## Installation Locale

PrÃ©requis:

- Python 3.12
- pip

Installation:

```bash
pip install -r requirements-dev.txt
```

CrÃ©er un fichier `.env` Ã  partir de `.env.example` si nÃ©cessaire:

```bash
cp .env.example .env
```

Variables Grok attendues:

```text
GROK_API_KEY=your_grok_api_key_here
GROK_MODEL=grok-2-latest
GROK_API_BASE_URL=https://api.x.ai/v1
```

Variables LangSmith optionnelles:

```text
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=finance-incident-multi-agent
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
```

Sans `LANGSMITH_API_KEY`, le tracing LangSmith est automatiquement desactive.

## Lancement Avec Uvicorn

```bash
uvicorn app.main:app --reload
```

API locale:

```text
http://localhost:8002
```

## Lancement Avec Docker

```bash
docker compose up --build
```

ArrÃªter les conteneurs:

```bash
docker compose down
```

Si Docker affiche `failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine`, Docker Desktop n'est pas demarre ou son moteur Linux n'est pas disponible. Ouvrir Docker Desktop, attendre `Docker Desktop is running`, puis verifier:

```powershell
docker version
```

Ensuite:

```powershell
docker build -t finance-incident-agent .
docker run -p 8002:8002 --env-file .env finance-incident-agent
```

## Tests Pytest

Lancer les tests:

```bash
pytest -v
```

Alternative portable:

```bash
python -m pytest -v
```

Les tests utilisent des mocks/stubs pour Ã©viter les appels externes Ã  Grok.

## Continuous Integration

Le projet utilise GitHub Actions pour valider automatiquement les principaux aspects techniques du service:

- `ci.yml`: exÃ©cute la suite pytest complÃ¨te sur `push` et `pull_request`.
- `api-tests.yml`: valide uniquement les endpoints FastAPI critiques: `/`, `/health`, `/analyze` et les payloads invalides.
- `agent-tests.yml`: valide le workflow multi-agent IA: `SupervisorAgent`, `RiskAgent`, `FraudAgent`, `ComplianceAgent` et `MonitoringAgent`.
- `langgraph-tests.yml`: valide l'orchestration LangGraph, la compilation du graph, l'exÃ©cution des nodes, la propagation du state et le final state.
- `monitoring-tests.yml`: valide les composants de monitoring IA: latence, tokens, coÃ»t, toxicitÃ©, hallucination, prompt injection, PII et health monitor.
- `governance-tests.yml`: valide les documents de gouvernance comme `agent_card.json` et `docs/RUNBOOK.md`.
- `coverage.yml`: gÃ©nÃ¨re les rapports de couverture `xml`, `html` et `term`, applique un seuil minimal de 70%, et publie `htmlcov/` comme artifact GitHub.
- `docker-build.yml`: vÃ©rifie que l'image Docker peut Ãªtre construite sur push vers `main`.
- `security.yml`: lance Bandit sur le dossier `app` pour dÃ©tecter les problÃ¨mes de sÃ©curitÃ© Python courants.
- `render-health.yml`: peut Ãªtre dÃ©clenchÃ© manuellement pour vÃ©rifier `/health` sur l'URL Render configurÃ©e via `RENDER_URL`.

## DÃ©ploiement Render

Le fichier `render.yaml` configure un service web Docker avec:

```yaml
runtime: docker
healthCheckPath: /health
```

Sur Render:

1. CrÃ©er un service depuis le dÃ©pÃ´t.
2. VÃ©rifier que le runtime Docker est utilisÃ©.
3. Configurer les variables d'environnement.
4. DÃ©ployer.
5. VÃ©rifier `/health`.

## Runbook Incident

Actions principales:

- VÃ©rifier `/health` si l'API ne rÃ©pond pas.
- Lire `correlation_id` dans chaque rÃ©ponse `/analyze`.
- Si `risk_level` est `high`, dÃ©clencher une revue humaine.
- Si `prompt_injection.detected` est vrai, ne pas faire confiance au texte brut.
- Si PII est dÃ©tectÃ©e, Ã©viter de copier les donnÃ©es sensibles dans les logs.
- Si l'API est down, vÃ©rifier les logs puis redÃ©marrer Docker.
- Sur Render, vÃ©rifier le statut du dÃ©ploiement, les logs et `/health`.

Voir aussi:

- `docs/RUNBOOK.md`
- `docs/OBSERVABILITY.md`
- `docs/GOVERNANCE.md`
- `docs/GLOBAL_DOCUMENTATION.md`
- `docs/TECHNICAL_DOCUMENTATION.md`

## Structure Du Projet

```text
finance-incident-multi-agent/
â”œâ”€â”€ app/
â”‚   â”œâ”€â”€ main.py
â”‚   â”œâ”€â”€ config.py
â”‚   â”œâ”€â”€ api/
â”‚   â”œâ”€â”€ agents/
â”‚   â”œâ”€â”€ graph/
â”‚   â”œâ”€â”€ monitoring/
â”‚   â”œâ”€â”€ schemas/
â”‚   â”œâ”€â”€ services/
â”‚   â””â”€â”€ utils/
â”œâ”€â”€ tests/
â”œâ”€â”€ docs/
â”œâ”€â”€ .github/workflows/
â”œâ”€â”€ agent_card.json
â”œâ”€â”€ Dockerfile
â”œâ”€â”€ docker-compose.yml
â”œâ”€â”€ render.yaml
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ requirements-dev.txt
â”œâ”€â”€ pytest.ini
â”œâ”€â”€ README.md
â”œâ”€â”€ .env.example
â””â”€â”€ .gitignore
```

## Project Versions

| Version | Name | Description |
|---|---|---|
| **v1.0.0** | Backend MVP | FastAPI + LangGraph multi-agent pipeline, Docker, CI/CD, 71 tests |
| **v1.1.0** | Frontend Dashboard | React + Vite visual interface, form, results panel, CORS |
| **v1.2.0** | Agent Chat Experience | Immersive conversational UI with progressive agent message reveal |
| **v1.3.0** | AI Security & Telemetry | Real PII, prompt injection, toxicity detection; live security badge |
| **v1.4.0** | Production Release | Complete versioning documentation; project ready for presentation |
| **v1.5.0** | Grok-Based AI Monitoring | Hybrid static + Grok safety pipeline, final decision, fallback |
| **v1.6.0** | LangSmith Observability | External LangGraph tracing, metadata, `/observability` endpoint |
| **v1.7.0** | LangSmith Observability UI | Frontend workflow, correlation_id, monitoring, metrics, LangSmith panels and connected chat |
| **v1.8.0** | Grok Chat & Supervision Docs | Real `/chat` endpoint with Grok, frontend supervision platform, global and technical documentation |

See [`docs/VERSIONING.md`](docs/VERSIONING.md) for the full versioning strategy, [`docs/CHANGELOG.md`](docs/CHANGELOG.md) for the detailed feature log, and [`docs/RELEASE_NOTES.md`](docs/RELEASE_NOTES.md) for user-facing release summaries.

## Release Timeline

```text
v1.0.0 -> Backend MVP
          FastAPI, LangGraph, 4 agents, Docker, CI workflows, 71 tests

v1.1.0 -> Frontend Dashboard
          React + Vite, incident form, result dashboard, metrics panel, CORS

v1.2.0 -> Agent Chat Experience
          Agent chat UI, progressive reveal, thinking animation

v1.3.0 -> AI Security & Telemetry
          Real PII, prompt injection, toxicity, live security badge

v1.4.0 -> Production Release
          VERSIONING.md, CHANGELOG.md, RELEASE_NOTES.md, architecture docs

v1.5.0 -> Grok-Based AI Monitoring
          Hybrid static + Grok safety pipeline, final_decision, fallback mode

v1.6.0 -> LangSmith Observability
          LangGraph tracing, finance_incident_analysis run, /observability endpoint

v1.7.0 -> LangSmith Observability UI
          Frontend supervision panels, workflow timeline, monitoring center

v1.8.0 -> Grok Chat & Documentation
          POST /chat with Grok, contextual assistant, global and technical docs
```

## Statut DÃ©mo

Ce projet est adaptÃ© Ã  une dÃ©monstration de fin de semaine: il prÃ©sente une API complÃ¨te, une orchestration multi-agent avec LangGraph, une couche d'observabilitÃ©, des rÃ¨gles de gouvernance, Docker, CI/CD et une suite de tests automatisÃ©s.

## Lien deploy 

back : https://analyze-incident-finance-production.up.railway.app/
front : https://finance-incident-multi-agent-production.up.railway.app/
