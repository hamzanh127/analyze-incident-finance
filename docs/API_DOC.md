# API Documentation

## Base URL

Local development:

```text
http://localhost:8002
```

## GET /

Returns service metadata.

```json
{
  "service": "finance-incident-multi-agent",
  "version": "1.0.0",
  "status": "running"
}
```

## GET /health

Returns service and agent health.

Expected status:

```json
{
  "service": "finance-incident-multi-agent",
  "status": "healthy",
  "agents": {}
}
```

## GET /metrics

Returns in-memory metrics.

```json
{
  "total_requests": 0,
  "total_errors": 0,
  "total_high_risk": 0,
  "total_manual_review": 0,
  "total_blocked": 0,
  "average_latency_ms": 0.0
}
```

## POST /analyze

Analyzes a financial incident.

Request:

```json
{
  "customer_id": "cust_123",
  "incident_type": "wire_transfer",
  "amount": 12500.0,
  "currency": "USD",
  "country": "US",
  "device": "mobile",
  "beneficiary_status": "new",
  "description": "Customer reports an unauthorized transfer."
}
```

Response:

```json
{
  "correlation_id": "FIN-20260626-ABC123",
  "risk_level": "high",
  "risk_score": 90,
  "fraud_suspicion": true,
  "fraud_score": 85,
  "compliance_status": "escalation_required",
  "decision": "blocked",
  "recommendations": [],
  "monitoring": {},
  "report": {}
}
```

Validation errors return HTTP `422`.
