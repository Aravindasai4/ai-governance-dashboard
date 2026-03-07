# AI Governance Dashboard for Loan Decision Systems

A production-grade observability and governance platform for monitoring automated AI loan decision systems. Provides real-time transparency into decision quality, data drift, human oversight effectiveness, and regulatory compliance.

## Overview

This dashboard addresses critical gaps in AI governance for high-stakes automated decision systems:

- **Decision Opacity**: Makes every automated loan decision auditable with full reason-code transparency
- **Model Degradation**: Detects input distribution shifts that indicate model performance decay
- **Accountability Gaps**: Tracks human-in-the-loop controls to verify oversight mechanisms are functioning
- **Undetected Errors**: Continuous measurement of false positive and false negative rates in production
- **Contract Drift**: Live inspection of decision contracts to verify operational compliance

Built as a governance layer over an AI loan simulator, this system demonstrates end-to-end implementation of AI risk management principles in a financial services context.

## Key Features

### Decision Observability
- Real-time monitoring of every automated decision (APPROVE/REVIEW/REJECT)
- Full transparency into risk scores, reason codes, and model versions
- 24-hour and 7-day decision volume tracking with outcome distributions
- Recent decisions table with drill-down to individual decision records

### Data Drift Detection
- Tracks distribution shifts in critical input features (credit score, income, DTI ratio)
- Baseline comparison against training data distributions
- Color-coded severity thresholds (green/yellow/red) for drift magnitude
- Dual-axis time-series visualization for trend analysis

### Human-in-the-Loop Monitoring
- Review rate tracking against configurable thresholds (15%/30%/50%)
- Human override count and pattern analysis
- Pending review queue monitoring for operational bottlenecks
- Visual gauge display with threshold-based alerting

### Decision Quality Assurance
- **Slips**: False negatives (engine approved, later found problematic)
- **Corrections**: False positives (engine rejected, later found acceptable)
- Continuous measurement of Type I and Type II error rates
- Feedback loop for ongoing model quality assessment

### Contract Compliance
- Inspectable AI Decision Contract defining:
  - Formal decision type schemas
  - Input/output field specifications
  - Reason code taxonomy
  - Risk threshold definitions
  - SLA commitments
- Version-controlled contract tracking
- Recursive JSON renderer for contract navigation

### Data Quality Auditing
- Measures decision explanation completeness
- Tracks event-decision linkage integrity
- Surfaces missing or malformed governance metadata
- Audit trail validation

### Alerting & Anomaly Detection
- System-generated alerts for review rate spikes, distribution shifts, and operational anomalies
- Severity-graded alert display (WARN/CRITICAL/INFO)
- Real-time alert feed with contextual metadata

## Technical Architecture

### Stack
- **Backend**: Python 3, Flask, SQLite
- **Frontend**: Vanilla JavaScript, Chart.js v4.4.1, Pure CSS (no framework)
- **Integration**: Reverse proxy pattern for CORS-free API consumption
- **Data Flow**: Real-time aggregation from upstream decision API

### System Components

```
AI Loan Simulator API          →    Flask Proxy Layer    →    Browser Client
/api/measure/summary                 /proxy/measure_summary      fetch() + aggregate
/api/decisions                       /proxy/decisions             Chart.js render
/api/events                          /proxy/events                DOM manipulation
/api/alerts                          /proxy/alerts                
/api/contract                        /proxy/contract              
```

### Architecture Highlights

**Zero-Build Frontend**  
Entire observability UI built with vanilla JS and CSS. No bundler, no npm dependencies, no framework overhead. Five interactive charts, gauge displays, filtered tables, and collapsible sections using only CDN-loaded Chart.js.

**Client-Side Time-Series Aggregation**  
Hourly and daily charts computed client-side from raw decision records. Parses ISO 8601 timestamps into hour/day buckets, pre-initializes expected time slots, and counts by decision type. Works independently of upstream API aggregation capabilities.

**Dual-Axis Drift Visualization**  
Credit score (absolute scale ~600-700) and DTI ratio (ratio scale ~0.5-1.0) rendered on independent Y-axes for meaningful visual comparison despite different value ranges.

**Structured Error Handling**  
Proxy layer differentiates between timeout, connection, HTTP status, and parse errors. Returns structured JSON errors that render as user-friendly banners identifying specific failing endpoints.

**Recursive Contract Renderer**  
Introspects JSON types to produce collapsible sections for objects, pill badges for arrays, color-coded literals for primitives, and nested indentation for depth. Transforms raw JSON contracts into navigable documentation.

**Three-Tier Configuration**  
Source URL resolution: Environment variable → SQLite persisted setting → hardcoded default. Supports both ops-level and user-level configuration without code changes.

## Governance Methodologies Implemented

### Human-in-the-Loop Monitoring
Tracks review rate, override count, and pending queue to verify oversight controls are functioning and not being systematically bypassed.

### Slip/Correction Framework
Implements continuous model quality feedback loop distinguishing false negatives (slips) from false positives (corrections). Maps directly to Type I/Type II error framework for statistical rigor.

### Data Drift Monitoring
Monitors input feature distribution shifts against training baselines for credit score, income, and DTI. Follows ML production monitoring principle that input drift is a leading indicator of output degradation.

### Decision Contract Governance
Treats AI decision contracts as first-class artifacts with dedicated inspection views. Supports principle that AI systems should operate under explicitly declared, version-controlled behavioral contracts.

### Decision Explainability
Every decision surfaces reason codes (DTI_HIGH, CREDIT_SCORE_LOW, EMPLOYMENT_SHORT, LOW_RISK) with impact scores. Supports post-hoc explainability requirements for regulatory compliance.

### Data Quality Monitoring
Measures completeness of decision explanations and event-decision linkage. Validates audit trail integrity for compliance and forensic analysis.

## Dashboard Views

### Main Dashboard
- 8-card KPI overview (total decisions, review rate, overrides, slips, corrections, risk scores, pending queue)
- Decisions per Hour (24h) - Multi-series line chart
- Decisions per Day (7d) - Stacked bar chart
- Top Reason Codes (7d) - Horizontal bar chart
- Drift Over Time (7d) - Dual-axis line chart
- Review Rate Gauge - Threshold-based visual alerting
- Alerts Panel - Severity-badged alert feed
- Drift Deltas - Color-coded shift indicators
- Recent Decisions Table - 20-row detailed decision log

### Measure View
- Windowed metrics (24h/7d/all-time)
- Metric definitions and methodology
- Data quality audit results

### Contract View
- Full AI Decision Contract inspection
- Collapsible JSON sections
- Schema definitions and thresholds
- Version tracking

### Raw Data View
- Tabbed data explorer (Events/Decisions/Alerts)
- Text-based filtering
- Full field-level detail

### Settings View
- Source URL configuration
- 5-endpoint connection health check
- Connectivity diagnostics

## Design System

- **Theme**: Dark observability aesthetic optimized for dashboard monitoring
- **CSS Variables**: Consistent color system (`--bg`, `--bg-card`, `--accent`, `--text-primary`, `--text-secondary`)
- **Responsive Grid**: CSS Grid with 1fr 360px layout, collapses to single-column at 1100px
- **Components**: Pill badges, severity indicators, collapsible sections, gradient cards
- **Breakpoints**: 1100px (layout collapse), 600px (KPI card reflow)

## Use Cases

### AI Risk Management Teams
- Monitor automated decision systems for compliance with risk policies
- Detect model degradation before it impacts business outcomes
- Validate human oversight controls are functioning as designed

### Model Validation & Audit
- Continuous validation of production model performance
- Audit trail generation for regulatory examinations
- Contract compliance verification

### MLOps & Production ML Teams
- Data drift detection for model retraining triggers
- Decision volume and latency monitoring
- Operational health checks for decision pipelines

### Compliance & Legal
- Decision explainability for fair lending compliance
- Audit trail integrity validation
- Documentation of decision governance controls

## Technical Achievements

- **Zero-dependency frontend**: Production-grade dashboard with no build step, no npm, no framework
- **Real-time aggregation**: Client-side time-series bucketing from raw records
- **Structured observability**: Enterprise-grade error handling and diagnostics
- **Governance-first design**: Every feature maps to specific AI risk management principle

## Future Enhancements

- Bias metrics (demographic parity, equalized odds)
- Model performance tracking (precision, recall, F1 by outcome)
- Counterfactual explanations for individual decisions
- A/B testing support for model version comparison
- Automated drift threshold tuning
- Integration with incident management systems

---

**Built with**: Python, Flask, Chart.js, SQLite  
**Domain**: AI Governance, Risk Management, MLOps  
**Focus**: Transparency, Accountability, Compliance

## Repository Structure

```
ai-governance-dashboard/
├── main.py                 # Flask app + proxy layer
├── governance.db          # SQLite settings store
├── templates/
│   ├── base.html         # Design system + nav
│   ├── dashboard.html    # Main observability view
│   ├── measure.html      # Metrics + definitions
│   ├── contract.html     # Contract inspection
│   ├── raw.html          # Data explorer
│   └── settings.html     # Configuration
└── README.md
```
