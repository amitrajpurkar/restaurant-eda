<!--
Sync Impact Report:
- Version: 0.0.0 → 1.0.0 (Initial constitution ratification)
- Added Principles: Code Quality First, Test-Driven Development, Performance by Design, 
  API Contract Discipline, Observability & Monitoring
- Added Sections: Performance Standards, Development Workflow
- Templates Status:
  ✅ plan-template.md - Constitution Check section aligns with principles
  ✅ spec-template.md - Requirements section supports quality gates
  ✅ tasks-template.md - Test-first workflow matches TDD principle
- Follow-up: None - all placeholders filled
-->

# Restaurant EDA Web Application Constitution

## Core Principles

### I. Code Quality First (NON-NEGOTIABLE)

**All code MUST meet quality standards before merge:**

- **Type Safety**: Python code MUST use type hints (PEP 484); mypy strict mode MUST pass with zero errors
- **Linting**: Code MUST pass ruff linter with zero violations; Black formatting enforced
- **Code Review**: Every PR requires at least one approval; reviewers MUST verify constitution compliance
- **Complexity Limits**: Functions >50 lines require justification; cyclomatic complexity >10 requires refactoring
- **Documentation**: All public APIs MUST have docstrings (Google style); README MUST be current

**Rationale**: Quality issues compound over time. Enforcing standards early prevents technical debt and ensures maintainability as the codebase grows.

### II. Test-Driven Development (NON-NEGOTIABLE)

**Tests MUST be written before implementation:**

- **Red-Green-Refactor**: Write failing test → Implement minimal code → Refactor → Repeat
- **Coverage Minimum**: 80% code coverage required; critical paths (auth, data processing) require 95%
- **Test Types Required**:
  - **Unit Tests**: All business logic, data transformations, utility functions
  - **Integration Tests**: API endpoints, database operations, external service calls
  - **Contract Tests**: All API endpoints MUST have contract tests validating request/response schemas
- **Test Isolation**: Tests MUST be independent; no shared state between tests
- **CI Gate**: All tests MUST pass before merge; no exceptions

**Rationale**: TDD ensures code is testable by design, catches regressions early, and serves as living documentation. The discipline prevents bugs from reaching production.

### III. Performance by Design

**Performance requirements MUST be defined upfront and validated:**

- **Response Time**: API endpoints MUST respond within 200ms (p95) for simple queries, 1s for complex analytics
- **Throughput**: Backend MUST handle 1000 requests/second under normal load
- **Resource Limits**: Backend services MUST operate within 512MB memory; database queries optimized for <100ms
- **Frontend Performance**: Initial page load <2s; Time to Interactive <3s; Lighthouse score >90
- **Monitoring**: All endpoints instrumented with timing metrics; performance regressions trigger alerts

**Rationale**: Performance cannot be bolted on later. Defining targets early ensures architectural decisions support scalability and user experience.

### IV. API Contract Discipline

**All API contracts MUST be explicit, versioned, and validated:**

- **Schema Definition**: All endpoints MUST have Pydantic models defining request/response schemas
- **Validation**: Input validation MUST happen at API boundary; reject invalid requests with 400 + clear error messages
- **Versioning**: Breaking changes require new API version (e.g., /api/v2/); backward compatibility maintained for 1 major version
- **Documentation**: OpenAPI/Swagger spec MUST be auto-generated and kept current; examples required for all endpoints
- **Contract Tests**: Every endpoint MUST have contract tests ensuring schema compliance

**Rationale**: Clear contracts prevent integration issues, enable parallel frontend/backend development, and make breaking changes explicit and manageable.

### V. Observability & Monitoring

**Systems MUST be observable in production:**

- **Structured Logging**: All logs MUST use structured format (JSON); include correlation IDs for request tracing
- **Metrics**: Track request rate, error rate, latency (p50/p95/p99) for all endpoints; business metrics (e.g., analysis completions)
- **Error Tracking**: All exceptions logged with full context; critical errors trigger alerts
- **Health Checks**: All services MUST expose /health endpoint; dependencies checked and reported
- **Debugging**: Logs MUST include sufficient context to debug issues without reproducing; no sensitive data in logs

**Rationale**: Production issues are inevitable. Observability enables rapid diagnosis and resolution, minimizing downtime and user impact.

## Performance Standards

### Backend Performance Requirements

- **API Latency**: p95 <200ms for CRUD operations, p95 <1s for analytics queries
- **Database**: Query execution <100ms; connection pool sized for 100 concurrent connections
- **Memory**: Services operate within 512MB RAM under normal load; graceful degradation under pressure
- **Concurrency**: Support 1000 concurrent users; horizontal scaling via stateless design

### Frontend Performance Requirements

- **Load Time**: First Contentful Paint <1.5s, Time to Interactive <3s on 3G connection
- **Bundle Size**: Initial JS bundle <200KB gzipped; code splitting for routes
- **Rendering**: 60fps during interactions; React DevTools profiler shows <16ms render times
- **Caching**: Static assets cached with versioned URLs; API responses cached where appropriate

### Data Processing Performance

- **EDA Operations**: Dataset loading <5s for 100K rows; visualization rendering <2s
- **ML Model**: Training time <10 minutes for LSTM model; inference <100ms per prediction
- **Batch Processing**: Handle datasets up to 1M rows; progress reporting for long operations

## Development Workflow

### Code Review Process

1. **Pre-Review Checklist**:
   - All tests pass locally and in CI
   - Code coverage meets minimum threshold
   - Linting and type checking pass
   - Performance benchmarks run (if applicable)
   - Documentation updated

2. **Review Requirements**:
   - At least one approval from code owner
   - Reviewer MUST verify constitution compliance
   - Reviewer MUST test functionality locally for significant changes
   - Security review required for authentication, authorization, data handling changes

3. **Merge Criteria**:
   - All CI checks green
   - Required approvals obtained
   - No unresolved review comments
   - Branch up-to-date with main

### Quality Gates

**Pre-Commit**:
- Linting (ruff) passes
- Type checking (mypy) passes
- Unit tests pass
- Code formatted (Black)

**Pre-Merge (CI)**:
- All tests pass (unit + integration + contract)
- Code coverage ≥80%
- Performance benchmarks within acceptable range
- Security scan passes (no high/critical vulnerabilities)
- Documentation builds successfully

**Pre-Deploy**:
- Staging deployment successful
- Smoke tests pass
- Performance tests pass
- Rollback plan documented

### Testing Strategy

**Test Pyramid**:
- **70% Unit Tests**: Fast, isolated, test business logic
- **20% Integration Tests**: Test component interactions, database, external services
- **10% Contract Tests**: Validate API contracts, ensure frontend/backend compatibility

**Test Organization**:
```
tests/
├── unit/           # Fast, isolated tests
├── integration/    # Database, API, service integration
├── contract/       # API contract validation
└── performance/    # Load tests, benchmarks
```

## Governance

### Constitution Authority

- This constitution supersedes all other development practices and guidelines
- All team members MUST be familiar with and follow these principles
- Violations MUST be justified in writing and approved by technical lead
- Regular compliance audits conducted quarterly

### Amendment Process

1. **Proposal**: Document proposed change with rationale and impact analysis
2. **Review**: Team review and discussion (minimum 1 week comment period)
3. **Approval**: Requires consensus from technical leads
4. **Migration**: Update all affected templates, documentation, and code
5. **Version**: Increment version following semantic versioning

### Complexity Justification

When constitution principles cannot be met:
- Document the specific violation in plan.md Complexity Tracking section
- Explain why the violation is necessary
- Document what simpler alternatives were considered and why they were rejected
- Obtain approval from technical lead before proceeding

### Compliance Verification

- **Code Reviews**: Reviewers MUST verify constitution compliance
- **CI Checks**: Automated checks enforce linting, typing, testing, coverage requirements
- **Quarterly Audits**: Review codebase for compliance; address violations
- **Onboarding**: New team members MUST review constitution as part of onboarding

**Version**: 1.0.0 | **Ratified**: 2025-11-12 | **Last Amended**: 2025-11-12
