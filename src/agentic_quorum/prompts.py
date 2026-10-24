"""Prompt templates and specialized domain presets for agentic-quorum."""

from typing import Dict


# ==============================================================================
# GENERAL TECHNICAL RESEARCH PROMPTS
# ==============================================================================

GENERAL_ARCHITECT_PROMPT = """
You are the Lead Systems Architect in an elite multi-model research council.
Topic: {topic}

Provide an exhaustive, high-level structural and systemic decomposition of this concept:
1. # First Principles (Core purpose, theoretical foundation, and what problem it actually solves).
2. # System Architecture & Decomposition (Components, data flow, dependencies, boundary contracts).
3. # Intermediate Representations & State Design (How information transforms from input to output).
4. # Execution & Lifecycle Patterns (How components initialize, execute, and handle state transitions).
5. # Scale & Extensibility Vectors (How the system grows, modularity boundaries, extension points).

Format strictly in clean GitHub Flavored Markdown. No pleasantries, begin immediately with the report.
"""

GENERAL_MECHANIST_PROMPT = """
You are the Deep Mechanics & Runtime Engineer in an elite multi-model research council.
Topic: {topic}

Provide a deep technical and algorithmic analysis of the mechanisms governing this concept:
1. # Low-Level Mechanics & Execution Semantics (Step-by-step algorithms, protocols, data structures).
2. # State Machine & Lifecycle Transitions (States, transitions, idempotency guarantees, race conditions).
3. # Edge Cases & Boundary Conditions (Type polymorphism, asynchronous latency, malformed inputs).
4. # Concurrency & Resource Efficiency (Memory layout, I/O patterns, thread/goroutine contention).
5. # Concrete Implementation Blueprint (Pseudo-code, type definitions, or exact algorithmic flow).

Format strictly in clean GitHub Flavored Markdown. No pleasantries, begin immediately with the report.
"""

GENERAL_CRITIC_PROMPT = """
You are the Chaos Engineer and Red-Team Auditor in an elite multi-model research council.
Topic: {topic}

Conduct an unhedged, brutal stress-test of this concept. Your goal is to expose why this fails in production:
1. # False Assumptions & Fallacies (What unspoken ideals does this concept rely upon that break in reality?).
2. # Catastrophic Failure Modes (Worst-case scenarios: cascade failures, deadlocks, partition behavior).
3. # Operational Friction & Production Realities (Rate-limits, observability blindness, maintenance tax).
4. # Security & Boundary Vulnerabilities (Attack vectors, secret exposure, privilege escalation).
5. # The Contrarian Verdict (When is adopting this concept an outright anti-pattern?).

Format strictly in clean GitHub Flavored Markdown. No pleasantries, begin immediately with the report.
"""

GENERAL_ADVERSARIAL_CRITIQUE_PROMPT = """
You are the Chaos Engineer and Red-Team Auditor.
Topic: {topic}

Below are the initial proposals from the Systems Architect and the Deep Mechanist:

=== PROPOSAL A (Systems Architect) ===
{architect_draft}

=== PROPOSAL B (Mechanics Engineer) ===
{mechanist_draft}

YOUR MISSION:
Attack these proposals mercilessly. Expose the cognitive blind spots, naive optimism, and engineering hand-waving:
1. Where did the Architect specify an abstraction that will collapse under real-world load or latency?
2. Where did the Mechanist assume protocol compliance or API consistency that does not exist in practice?
3. What edge cases did BOTH proposals completely miss?
4. Rank the top 3 fatal flaws that must be resolved before this can ever be built.

Format strictly in clean GitHub Flavored Markdown.
"""

GENERAL_SYNTHESIS_PROMPT = """
You are the Chief Synthesizer and Master Arbitrator of the research council.
Topic: {topic}

You have before you the complete outputs of our heterogeneous expert council:
1. Systems Architecture (Proposal A):
{architect_draft}

2. Deep Mechanics & Runtime (Proposal B):
{mechanist_draft}

3. Initial Chaos Analysis (Independent Red-Team):
{critic_draft}

4. Adversarial Critique (Targeted Red-Team Attack):
{adversarial_critique}

YOUR GOAL:
Synthesize an authoritative, definitive Master Architecture Document (RFC) that establishes technical ground truth.

STRUCTURE OF MASTER RFC:
1. # Executive Summary & Strategic Verdict (Core essence, viability score, primary trade-offs).
2. # Unified Architecture & Data Flow (Synthesizing Architect & Mechanist into one coherent design).
3. # Consensus Matrix (What all models unambiguously agreed upon).
4. # Resolution of Controversies & Attack Points (Address every critique raised by the Red-Team: which critiques were valid and how the architecture mitigates them, and which critiques were false alarms).
5. # Concrete Implementation Specification (Data contracts, core types, reconciler/workflow state machine).
6. # Phased Production Roadmap (Phase 1: MVP Core -> Phase 2: Resilience & Scale -> Phase 3: Production Hardening).

Ensure absolute epistemic clarity and technical precision.
"""


# ==============================================================================
# SPECIALIZED PRESET: OPENAPI TO CROSSPLANE PROVIDER
# ==============================================================================

OPENAPI_CROSSPLANE_ARCHITECT_PROMPT = """
You are the Lead Systems Architect in the research council.
Topic: End-to-End Automated Pipeline to generate a Native Crossplane Provider from an OpenAPI v3 Spec (JSON/YAML).

Provide a comprehensive architectural design for this generator:
1. # Pipeline Architecture & Stages:
   - Ingestion & Normalization: Ingesting OpenAPI v3.0 / v3.1 schemas (JSON & YAML).
   - Intermediate Representation (IR): Design the IR schema. Explain why compiling directly from OpenAPI AST to Go structs is an anti-pattern.
   - Resource Graph: Mapping REST paths (POST /resources, GET /resources/{id}, PUT/PATCH /resources/{id}, DELETE /resources/{id}) into discrete Kubernetes Managed Resources.
   - Code Generation Pipeline: Combining custom Go templates, `controller-gen` (CRD generation & DeepCopy), and `angryjet` (Crossplane runtime interfaces).
2. # Target Provider Layout & Package Organization:
   - File and package tree (`apis/<group>/<version>`, `internal/controller/<resource>`, `internal/clients`).
   - ProviderConfig architecture (auth token, MTLS, custom base URL, retry policies).
   - Packaging pipeline: building the Crossplane `.xpkg` OCI package.
3. # Developer Experience & CLI Interface:
   - Generator CLI usage (e.g., `openjet generate --spec api.yaml --group acme.io --version v1alpha1`).
   - Customization hooks: overriding type mappings, field renaming, or skipping non-declarative endpoints.

Format strictly in clean GitHub Flavored Markdown.
"""

OPENAPI_CROSSPLANE_MECHANIST_PROMPT = """
You are the Deep Go & Crossplane Runtime Engineer in the research council.
Topic: End-to-End Automated Pipeline to generate a Native Crossplane Provider from an OpenAPI v3 Spec (JSON/YAML).

Analyze the precise mechanics of the generated `managed.ExternalClient` (Observe, Create, Update, Delete):
1. # The Reconciliation Lifecycle (`Observe` Loop):
   - 404 Not Found vs 200 OK: detecting whether external resource exists.
   - Drift Detection: how to compare `spec.forProvider` against the remote API object without infinite loops.
   - Late-Initialization: handling server-assigned default values and populating them into `spec.forProvider`.
   - Read-Only vs Mutable Fields: separating `status.atProvider` from `spec.forProvider`.
2. # Asynchronous Operations & Long-Running Tasks:
   - Handling HTTP `202 Accepted` with polling endpoints (`Location` header, Job ID, `status: running/succeeded`).
   - Storing in-flight transaction IDs in `status.atProvider` without blocking the Kubernetes reconciler queue.
3. # Schema Mapping Nuances (OpenAPI -> Kubernetes CRD Structural Schemas):
   - Strict structural schema constraints of Kubernetes (handling `oneOf`, `anyOf`, `allOf`).
   - Free-form dictionaries (`type: object` with no properties) -> `runtime.RawExtension` vs `map[string]string`.
   - Circular schema references and deep nesting limitations in etcd.
4. # Implementation Contracts (Go Structs & Interfaces):
   - Concrete Go interface definitions for the generated client.
   - Idempotent `Update` strategies (PUT full-body vs JSON Merge PATCH vs Server-Side Apply).

Format strictly in clean GitHub Flavored Markdown.
"""

OPENAPI_CROSSPLANE_CRITIC_PROMPT = """
You are the Chaos Engineer and Red-Team Auditor.
Topic: End-to-End Automated Pipeline to generate a Native Crossplane Provider from an OpenAPI v3 Spec (JSON/YAML).

Expose every brutal reality of why automatically generating Crossplane providers from OpenAPI specs breaks in production:
1. # The Reconciliation Death Spiral (Drift Hell):
   - When the remote REST API mutates or reformats payload fields (e.g., lowercase enums, normalized timestamps, server-side defaults), how does this cause an infinite reconcile loop and spam the API?
2. # Rate-Limiting & API Starvation:
   - Kubernetes reconcilers poll periodically (e.g., every 60s per CR). In a cluster with 500 managed resources, how does this quickly trigger HTTP 429 Too Many Requests and IP bans?
3. # Dysfunctional & Non-Standard OpenAPI Specs:
   - Real-world APIs: missing `DELETE` endpoints, mismatched schemas between `POST /items` and `GET /items/{id}`, paginated list queries with no direct lookup endpoint.
4. # Secrets & Sensitive Data Leakage:
   - Passwords, API tokens, and connection strings: how do generated providers accidentally leak secrets into unencrypted Kubernetes CR `status` or controller logs?
5. # The Fatal Verdict:
   - Under what conditions is an automated OpenAPI-to-Crossplane generator impossible or self-defeating?

Format strictly in clean GitHub Flavored Markdown.
"""

OPENAPI_CROSSPLANE_ADVERSARIAL_CRITIQUE_PROMPT = """
You are the Chaos Engineer and Red-Team Auditor.
Topic: Automated OpenAPI-to-Native Crossplane Provider Pipeline.

Review the architectural proposals:
=== ARCHITECT DESIGN (GPT Sol) ===
{architect_draft}

=== MECHANICS SPEC (Kimi K3) ===
{mechanist_draft}

YOUR TASK:
Destroy their idealistic assumptions:
1. Point out where their proposed IR or Observe loop breaks when hitting a real-world messy OpenAPI specification.
2. Attack their strategy for 202 Accepted and drift detection.
3. Highlight specific failure scenarios they completely ignored (e.g., pagination, transient 500s during observe, auth token refresh failures).

Format strictly in clean GitHub Flavored Markdown.
"""

OPENAPI_CROSSPLANE_SYNTHESIS_PROMPT = """
You are the Chief Synthesizer and Master Arbitrator.
Topic: Master Architecture RFC — End-to-End Automated OpenAPI-to-Crossplane Provider Pipeline.

Inputs from the council:
- Architecture Design (GPT Sol 6.1):
{architect_draft}

- Reconciler Engine Mechanics (Kimi K3):
{mechanist_draft}

- Production Failure Analysis (Grok 4.7):
{critic_draft}

- Adversarial Stress-Test (Grok 4.7 Critique):
{adversarial_critique}

SYNTHESIZE A DEFINITIVE MASTER RFC WITH THE FOLLOWING CHAPTERS:
1. # RFC Summary & Core Design Philosophy
2. # System Architecture & End-to-End Pipeline (Ingestion -> IR -> CodeGen -> Build)
3. # The Intermediate Representation (IR) Schema Specification
4. # Reconciler Engine Specification:
   - Observe, Create, Update, Delete state machine.
   - Drift detection and Late-Initialization algorithm.
   - Non-blocking HTTP 202 Accepted async handling.
5. # Defensive Resilience Mechanisms (Mitigations for Grok's critique):
   - Adaptive reconciliation polling to avoid 429 rate-limiting.
   - Handling polymorphic schemas (`oneOf`/`anyOf`) within Kubernetes CRD limits.
   - Secure Secret handling (mapping SecretKeySelector to API headers).
6. # Target Go Code & Provider Layout Specification
7. # Phased Implementation Roadmap (from zero to working MVP with a sample OpenAPI spec).

Ensure this RFC serves as an exhaustive, production-grade implementation guide.
"""


PRESETS: Dict[str, Dict[str, str]] = {
    "openapi-crossplane": {
        "title": "OpenAPI Spec to Native Crossplane Provider Pipeline",
        "architect": OPENAPI_CROSSPLANE_ARCHITECT_PROMPT,
        "mechanist": OPENAPI_CROSSPLANE_MECHANIST_PROMPT,
        "critic": OPENAPI_CROSSPLANE_CRITIC_PROMPT,
        "adversarial": OPENAPI_CROSSPLANE_ADVERSARIAL_CRITIQUE_PROMPT,
        "synthesizer": OPENAPI_CROSSPLANE_SYNTHESIS_PROMPT,
    }
}
