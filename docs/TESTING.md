# Testing

## Test Command

Use:

```bash
pytest -v
```

If the `pytest` launcher is not available in your shell, use:

```bash
python -m pytest -v
```

## Test Scope

The test suite covers:

- API endpoints
- request validation
- risk agent
- fraud agent
- compliance agent
- supervisor agent
- LangGraph builder
- monitoring utilities
- metrics
- logs
- decision rules
- correlation id format

## External API Calls

Unit tests must not call Grok or any external API. Use mocks, stubs, or injectable services.

## Expected Result

A healthy run should complete with all tests passing:

```text
48 passed
```
