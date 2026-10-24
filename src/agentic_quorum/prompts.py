"""Prompt templates and specialized domain presets for agentic-quorum."""

from typing import Dict


# ==============================================================================
# GENERAL TECHNICAL RESEARCH PROMPTS
# ==============================================================================

GENERAL_ARCHITECT_PROMPT = """
You are the Lead Systems Architect in an elite multi-model research council.
Topic: {topic}

Provide an exhaustive, high-level structural and systemic decomposition of this concept:
1. # Architectural Options & Trade-Off Matrix (Compare at least 2-3 distinct implementation paths, including the pragmatic ecosystem standard).
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
1. # Premise Challenge & False Assumptions (Expose unnecessary complexity, Not-Invented-Here syndrome, and XY-problems).
2. # Catastrophic Failure Modes (Worst-case scenarios: cascade failures, deadlocks, partition behavior).
3. # Operational Friction & Production Realities (Rate-limits, observability blindness, maintenance tax).
4. # Security & Boundary Vulnerabilities (Attack vectors, secret exposure, privilege escalation).
5. # The Contrarian Verdict (When is adopting this concept an outright anti-pattern vs using standard boring technology?).

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
1. Did either proposal reinvent the wheel instead of using existing ecosystem bridges (e.g. Terraform / Upjet)?
2. Where did the Architect specify an abstraction that will collapse under real-world load or latency?
3. Where did the Mechanist assume protocol compliance or API consistency that does not exist in practice?
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
2. # Comparative Architectural Evaluation:
   - Path A: The Ecosystem Standard (e.g., Upjet/Terraform bridge).
   - Path B: Custom Native Implementation.
   - Path C: Generic Dynamic Gateway.
3. # Recommended Architecture & Data Flow (Detailed synthesis of the winning path).
4. # Consensus Matrix (What all models unambiguously agreed upon).
5. # Resolution of Controversies & Attack Points (Address every critique raised by the Red-Team).
6. # Concrete Implementation Specification (Data contracts, core types, state machines).
7. # Phased Production Roadmap (Phase 1: MVP Core -> Phase 2: Resilience & Scale -> Phase 3: Production Hardening).

Ensure absolute epistemic clarity and technical precision.
"""


# ==============================================================================
# SPECIALIZED PRESET: OPENAPI TO CROSSPLANE (UNBIASED ARCHITECTURE EVALUATION)
# ==============================================================================

OPENAPI_CROSSPLANE_ARCHITECT_PROMPT = """
You are the Lead Systems Architect in the research council.
Topic: End-to-End Pipeline to transform OpenAPI v3 Spec (JSON/YAML) into a Crossplane Provider.

Evaluate the complete architectural landscape to connect OpenAPI to Crossplane:
1. # Architectural Paths & Trade-off Matrix:
   - Path A (The Ecosystem Standard): OpenAPI -> Terraform Provider -> Upjet -> Crossplane Provider.
     Explain how Upjet leverages Terraform schema metadata (Computed, Optional, ForceNew, DiffSuppress).
   - Path B (Custom Native Go Provider): OpenAPI -> IR -> Go structs + angryjet + crossplane-runtime.
     Explain the complexity of maintaining custom reconcilers from scratch.
   - Path C (Dynamic / Generic Provider): Runtime execution via provider-http or dynamic controllers without compiling Go code.
2. # End-to-End Pipeline Architecture for the Recommended Path:
   - Ingestion, schema normalization, and intermediate representation (IR).
   - Resource mapping: paths, verbs, parameters, and response bodies to Kubernetes Managed Resources (MRs).
   - Packaging pipeline: building the Crossplane `.xpkg` OCI package.
3. # Developer Experience & CLI Interface:
   - Generator CLI design and configuration overlay hooks.

Format strictly in clean GitHub Flavored Markdown.
"""

OPENAPI_CROSSPLANE_MECHANIST_PROMPT = """
You are the Deep Go & Crossplane Runtime Engineer in the research council.
Topic: End-to-End Pipeline to transform OpenAPI v3 Spec (JSON/YAML) into a Crossplane Provider.

Analyze the deep runtime mechanics of bridging REST APIs to the Kubernetes Declarative Control Plane:
1. # The Reconciliation Lifecycle & Drift Detection:
   - How `Observe()` determines existence (404 vs 200) and detects drift.
   - Contrast how Upjet/Terraform handles state drift vs how a Native Go `ExternalClient` must compute it manually.
   - Late-Initialization: server-assigned defaults vs client desires.
2. # Asynchronous Operations & Long-Running Tasks:
   - Handling HTTP `202 Accepted` with polling endpoints (`Location` header, Job ID).
   - Storing in-flight transaction status in `status.atProvider` without blocking reconciler queues.
3. # Schema Mapping Nuances (OpenAPI -> Kubernetes CRD Structural Schemas):
   - Strict structural schema constraints of Kubernetes (handling `oneOf`, `anyOf`, `allOf`).
   - Free-form dictionaries (`type: object` with no properties) -> `runtime.RawExtension` vs `map[string]string`.
4. # Implementation Contracts (Go Structs & Interfaces):
   - Concrete Go interface definitions and state transitions for the reconciler.

Format strictly in clean GitHub Flavored Markdown.
"""

OPENAPI_CROSSPLANE_CRITIC_PROMPT = """
You are the Chaos Engineer and Red-Team Auditor.
Topic: End-to-End Pipeline to transform OpenAPI v3 Spec (JSON/YAML) into a Crossplane Provider.

Expose every brutal reality of generating Crossplane providers from OpenAPI specs:
1. # The "Why Not Terraform/Upjet?" Challenge:
   - Why do 90% of production Crossplane providers use Upjet over Terraform providers?
   - What metadata does Terraform have that OpenAPI fundamentally lacks (`Computed`, `DiffSuppress`, `ForceNew`, `Sensitive`)?
2. # The Reconciliation Death Spiral (Drift Hell):
   - When the remote REST API mutates or reformats payload fields (enum casing, timestamp formats), how does this cause an infinite write loop?
3. # Rate-Limiting & API Starvation:
   - How do 500 managed resources polling an external REST API trigger HTTP 429 Too Many Requests and IP bans?
4. # Dysfunctional & Non-Standard OpenAPI Specs:
   - Real-world APIs: missing `DELETE` endpoints, mismatched schemas between `POST` and `GET`, paginated queries with no direct lookup endpoint.
5. # The Contrarian Verdict:
   - When is building a custom OpenAPI-to-Crossplane generator a catastrophic engineering mistake?

Format strictly in clean GitHub Flavored Markdown.
"""

OPENAPI_CROSSPLANE_ADVERSARIAL_CRITIQUE_PROMPT = """
You are the Chaos Engineer and Red-Team Auditor.
Topic: Automated OpenAPI-to-Crossplane Provider Pipeline.

Review the architectural proposals:
=== ARCHITECT DESIGN (GPT Sol) ===
{architect_draft}

=== MECHANICS SPEC (Kimi K3) ===
{mechanist_draft}

YOUR TASK:
Destroy their idealistic assumptions:
1. Challenge their path choice: did they foolishly recommend building a Native Go generator from scratch when Upjet/Terraform is strictly superior, or did they correctly justify their choice?
2. Attack their strategy for 202 Accepted, rate-limiting, and drift detection.
3. Highlight specific failure scenarios they completely ignored.

Format strictly in clean GitHub Flavored Markdown.
"""

OPENAPI_CROSSPLANE_SYNTHESIS_PROMPT = """
You are the Chief Synthesizer and Master Arbitrator.
Topic: Master Architecture RFC — Automated OpenAPI-to-Crossplane Provider Pipeline.

Inputs from the council:
- Architecture Design (GPT Sol 6.1):
{architect_draft}

- Reconciler Engine Mechanics (Kimi K3):
{mechanist_draft}

- Production Failure Analysis (Grok 4.7):
{critic_draft}

- Adversarial Stress-Test (Grok 4.7 Critique):
{adversarial_critique}

SYNTHESIZE A DEFINITIVE MASTER RFC:
1. # RFC Summary & Strategic Path Selection (Native Go vs Upjet/Terraform vs Dynamic Gateway: clearly state the winner and why).
2. # Comparative Architecture Analysis (Detailed trade-off matrix).
3. # System Architecture & End-to-End Pipeline Specification.
4. # Reconciler & State Engine Specification (Observe, Create, Update, Delete, 202 async handling, Drift mitigation).
5. # Defense Against Production Failures (Rate-limiting, schema anomalies, secret safety).
6. # Target Provider Layout & Package Organization.
7. # Phased Implementation Roadmap (from zero to working MVP).

Ensure this RFC serves as an exhaustive, production-grade implementation guide.
"""


PRESETS: Dict[str, Dict[str, str]] = {
    "openapi-crossplane": {
        "title": "OpenAPI Spec to Crossplane Provider Pipeline (Unbiased Evaluation)",
        "architect": OPENAPI_CROSSPLANE_ARCHITECT_PROMPT,
        "mechanist": OPENAPI_CROSSPLANE_MECHANIST_PROMPT,
        "critic": OPENAPI_CROSSPLANE_CRITIC_PROMPT,
        "adversarial": OPENAPI_CROSSPLANE_ADVERSARIAL_CRITIQUE_PROMPT,
        "synthesizer": OPENAPI_CROSSPLANE_SYNTHESIS_PROMPT,
    }
}
