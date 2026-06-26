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

`finance-incident-multi-agent` est un projet de formation backend Python conçu pour analyser des incidents financiers: virements suspects, transactions inhabituelles, nouveaux bénéficiaires, risques de fraude, contraintes AML/KYC et besoin de revue humaine.

Le projet illustre une architecture professionnelle avec FastAPI, Pydantic, LangGraph, agents IA spécialisés, monitoring IA, observabilité et tests automatisés.

## Objectif

L'objectif est de fournir une API capable de recevoir un incident financier, d'orchestrer plusieurs agents spécialisés, puis de retourner une décision structurée:

- `approved`
- `manual_review`
- `blocked`

Chaque analyse retourne aussi un `correlation_id`, des recommandations, un bloc de monitoring et un rapport final.

## Architecture Multi-Agent

L'orchestration est gérée par LangGraph.

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

`SupervisorAgent` ne lance pas directement les agents. Il génère un `correlation_id`, crée l'état initial, appelle le graph LangGraph compilé, puis formate la réponse finale compatible avec `AnalyzeResponse`.

## Rôle Des Agents

- `SupervisorAgent`: orchestre l'analyse via LangGraph et prépare la réponse API.
- `RiskAgent`: analyse le niveau de risque financier avec Grok.
- `FraudAgent`: détecte les signaux de fraude financière avec Grok.
- `ComplianceAgent`: évalue AML, KYC, gouvernance et besoin d'escalade conformité avec Grok.
- `MonitoringAgent`: suit l'exécution, le statut, la latence et les indicateurs d'observabilité.

## Monitoring IA

Le service inclut des contrôles IA simples, déterministes et testables:

- toxicité
- hallucination
- prompt injection
- PII
- estimation de tokens
- estimation de coût
- latence

Ces contrôles sont centralisés dans `app/monitoring`.

## Observabilité Et Correlation ID

Chaque analyse retourne un identifiant de corrélation:

```text
FIN-YYYYMMDD-XXXXXX
```

Exemple:

```json
{
  "correlation_id": "FIN-20260626-ABC123"
}
```

Ce `correlation_id` permet de relier une réponse API, un log, un événement d'observabilité et une investigation manuelle.

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

| Méthode | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Statut du service |
| `GET` | `/health` | Santé du service et des agents |
| `GET` | `/metrics` | Métriques en mémoire |
| `GET` | `/observability` | Configuration d'observabilite LangSmith |
| `POST` | `/analyze` | Analyse d'un incident financier |

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

Prérequis:

- Python 3.12
- pip

Installation:

```bash
pip install -r requirements-dev.txt
```

Créer un fichier `.env` à partir de `.env.example` si nécessaire:

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

Arrêter les conteneurs:

```bash
docker compose down
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

Les tests utilisent des mocks/stubs pour éviter les appels externes à Grok.

## Continuous Integration

Le projet utilise GitHub Actions pour valider automatiquement les principaux aspects techniques du service:

- `ci.yml`: exécute la suite pytest complète sur `push` et `pull_request`.
- `api-tests.yml`: valide uniquement les endpoints FastAPI critiques: `/`, `/health`, `/analyze` et les payloads invalides.
- `agent-tests.yml`: valide le workflow multi-agent IA: `SupervisorAgent`, `RiskAgent`, `FraudAgent`, `ComplianceAgent` et `MonitoringAgent`.
- `langgraph-tests.yml`: valide l'orchestration LangGraph, la compilation du graph, l'exécution des nodes, la propagation du state et le final state.
- `monitoring-tests.yml`: valide les composants de monitoring IA: latence, tokens, coût, toxicité, hallucination, prompt injection, PII et health monitor.
- `governance-tests.yml`: valide les documents de gouvernance comme `agent_card.json` et `docs/RUNBOOK.md`.
- `coverage.yml`: génère les rapports de couverture `xml`, `html` et `term`, applique un seuil minimal de 70%, et publie `htmlcov/` comme artifact GitHub.
- `docker-build.yml`: vérifie que l'image Docker peut être construite sur push vers `main`.
- `security.yml`: lance Bandit sur le dossier `app` pour détecter les problèmes de sécurité Python courants.
- `render-health.yml`: peut être déclenché manuellement pour vérifier `/health` sur l'URL Render configurée via `RENDER_URL`.

## Déploiement Render

Le fichier `render.yaml` configure un service web Docker avec:

```yaml
runtime: docker
healthCheckPath: /health
```

Sur Render:

1. Créer un service depuis le dépôt.
2. Vérifier que le runtime Docker est utilisé.
3. Configurer les variables d'environnement.
4. Déployer.
5. Vérifier `/health`.

## Runbook Incident

Actions principales:

- Vérifier `/health` si l'API ne répond pas.
- Lire `correlation_id` dans chaque réponse `/analyze`.
- Si `risk_level` est `high`, déclencher une revue humaine.
- Si `prompt_injection.detected` est vrai, ne pas faire confiance au texte brut.
- Si PII est détectée, éviter de copier les données sensibles dans les logs.
- Si l'API est down, vérifier les logs puis redémarrer Docker.
- Sur Render, vérifier le statut du déploiement, les logs et `/health`.

Voir aussi:

- `docs/RUNBOOK.md`
- `docs/OBSERVABILITY.md`
- `docs/GOVERNANCE.md`

## Structure Du Projet

```text
finance-incident-multi-agent/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── api/
│   ├── agents/
│   ├── graph/
│   ├── monitoring/
│   ├── schemas/
│   ├── services/
│   └── utils/
├── tests/
├── docs/
├── .github/workflows/
├── agent_card.json
├── Dockerfile
├── docker-compose.yml
├── render.yaml
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── README.md
├── .env.example
└── .gitignore
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

See [`docs/VERSIONING.md`](docs/VERSIONING.md) for the full versioning strategy, [`docs/CHANGELOG.md`](docs/CHANGELOG.md) for the detailed feature log, and [`docs/RELEASE_NOTES.md`](docs/RELEASE_NOTES.md) for user-facing release summaries.

## Release Timeline

```text
v1.0.0 ─── Backend MVP
  │         FastAPI · LangGraph · 4 Agents · Docker · 9 CI workflows · 71 tests
  │
  ▼
v1.1.0 ─── Frontend Dashboard
  │         React + Vite · IncidentForm · ResultDashboard · MetricsPanel · CORS
  │
  ▼
v1.2.0 ─── Agent Chat Experience
  │         AgentChat · AgentMessage · Progressive reveal · Thinking animation
  │
  ▼
v1.3.0 ─── AI Security & Telemetry
  │         Real PII · Prompt Injection (9 patterns) · French toxicity
  │         Live security badge · Tokens & cost from real data
  │
  ▼
v1.4.0 ─── Production Release
  │         VERSIONING.md · CHANGELOG.md · RELEASE_NOTES.md
  │         Updated ARCHITECTURE.md · README Release Timeline
  │
  ▼
v1.5.0 ─── Grok-Based AI Monitoring
            MonitoringService hybrid pipeline (static + Grok)
            Grok safety review · final_decision · fallback mode
            Frontend: [Static]/[Grok]/[Final] badges · 88 tests ✅
  │
  ▼
v1.6.0 ─── LangSmith Observability
            LangGraph tracing · finance_incident_analysis run
            Agent-step metadata · /observability endpoint
            Offline mocked tests · 93 tests ✅
```

## Statut Démo

Ce projet est adapté à une démonstration de fin de semaine: il présente une API complète, une orchestration multi-agent avec LangGraph, une couche d'observabilité, des règles de gouvernance, Docker, CI/CD et une suite de tests automatisés.
