# AI Governance Hub

## Overview
A Flask-based observability dashboard for monitoring AI loan decision systems. It provides a Kibana-like visual interface for tracking decisions, drift, alerts, and contract compliance.

## Architecture
- **Backend**: Python/Flask (main.py) with SQLite for settings storage
- **Frontend**: Jinja2 templates with Chart.js (CDN) for visualizations
- **Data Source**: Proxies requests to a configurable source API (default: https://loan-decision-contract.replit.app)
- **Database**: governance.db (SQLite) - auto-created, stores settings only

## Key Files
- `main.py` - Flask app with proxy endpoints and page routes
- `templates/base.html` - Base template with dark theme CSS, nav, and shared styles
- `templates/dashboard.html` - Primary dashboard with KPI cards, charts, alerts
- `templates/measure.html` - Detailed metrics with definitions and data quality
- `templates/contract.html` - Collapsible contract viewer
- `templates/raw.html` - Raw data tables with filters
- `templates/settings.html` - Source URL configuration and health check

## Proxy Endpoints
All browser requests go through `/proxy/*` to avoid CORS:
- `/proxy/measure_summary?window=24h|7d|all`
- `/proxy/alerts?limit=N`
- `/proxy/events?limit=N`
- `/proxy/decisions?limit=N`
- `/proxy/contract`

## Configuration
- `SOURCE_BASE_URL` env var overrides default
- `/settings` page stores URL in SQLite
- Default: https://loan-decision-contract.replit.app

## Running
- `python main.py` starts on port 5000
