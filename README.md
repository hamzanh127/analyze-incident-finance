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

## Endpoints API

| Méthode | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Statut du service |
| `GET` | `/health` | Santé du service et des agents |
| `GET` | `/metrics` | Métriques en mémoire |
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

## Statut Démo

Ce projet est adapté à une démonstration de fin de semaine: il présente une API complète, une orchestration multi-agent avec LangGraph, une couche d'observabilité, des règles de gouvernance, Docker, CI/CD et une suite de tests automatisés.
