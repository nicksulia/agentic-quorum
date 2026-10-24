# 🏛️ agentic-quorum

> **Multi-model consensus research engine.** Heterogeneous frontier models meeting for peer-reviewed, verified technical truth with a **Phase 0 Socratic Gatekeeper** against premature premise-locking.

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Orchestrator](https://img.shields.io/badge/orchestrator-GitHub%20Copilot%20CLI-black.svg)](https://github.com/features/copilot)

`agentic-quorum` eliminates single-model cognitive bias, corporate safety blind spots, and hallucinations by orchestrating a distributed council of frontier AI models across a **four-stage consensus protocol**:
1. **Phase 0**: Socratic Gatekeeper (Premise & XY-Problem audit via Grok 4.7)
2. **Phase 1**: Divergent Parallel Exploration (GPT Sol 6.1, Kimi K3, Grok 4.7)
3. **Phase 2**: Adversarial Cross-Critique (Red-Team attack via Grok 4.7)
4. **Phase 3**: Epistemic Convergence & Master Synthesis (Claude Sonnet 5.5)

---

## 🛡️ Phase 0: The Socratic Gatekeeper

The biggest failure mode in AI-assisted research is **Compliance Bias / Sycophancy**. If you ask an LLM: *"How do I generate a Native Crossplane provider from scratch?"*, it obediently designs an overcomplicated, doomed-to-fail generator instead of slapping you on the wrist and asking: *"Why aren't you using OpenAPI -> Terraform -> Upjet like 95% of the ecosystem?"*

**The Socratic Gatekeeper (powered by Grok 4.7)** audits your topic in ~10 seconds *before* launching the heavy swarm:
- **Premature Solution-Locking / XY-Problem**: Catches when you prescribe an anti-pattern solution instead of stating the high-level goal.
- **Not-Invented-Here (NIH) Syndrome**: Exposes attempts to reinvent existing ecosystem bridges.
- **Industry Reality Check**: Points out the pragmatic, battle-tested standard (e.g., Upjet).
- **Broadened Agenda**: Reformulates the prompt so the council explores real architectural trade-offs.

---

## 👥 The Quorum Council ("The Big Four")

| Node | Model Identifier | Frontier Lab | Specialized Role | Reasoning Effort | Primary Focus |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Gatekeeper** | `grok-4.7` | **xAI** | Socratic Gatekeeper & Auditor | `low` (fast) | Auditing user premises, catching XY problems, and forcing ecosystem trade-off evaluation. |
| **Architect** | `gpt-6.1-sol` | **OpenAI** | Systems Architect & Planner | `high` | Architectural options, trade-off matrix, pipeline decomposition, and lifecycle workflows. |
| **Mechanist** | `kimi-k3` | **Moonshot AI** | Deep Runtime & Mechanics | `high` | Reconciliation semantics, drift detection, 202 async polling, and Go type systems. |
| **Critic** | `grok-4.7` | **xAI** | Chaos Engineer & Red-Team | `high` | Production failure modes, rate-limiting (HTTP 429), drift loops, and unhedged stress-testing. |
| **Synthesizer** | `claude-sonnet-5.5` | **Anthropic** | Chief Synthesizer & Arbitrator | `high` | Epistemic arbitration, resolving disagreements, and compiling the master RFC. |

---

## 🔄 The Protocol Workflow

```
                        [User Topic / Request]
                                  │
                                  ▼
                   [Phase 0: Socratic Gatekeeper]
                             (Grok 4.7)
                   Audits premise, flags XY-problems
                                  │
            ┌─────────────────────┴─────────────────────┐
            ▼                                           ▼
 [Anchoring Detected!]                         [Clean Premise]
  • Wrist-slap & reality check                          │
  • Viable alternatives presented                       │
  • User confirms / broadens scope                      │
            │                                           │
            └─────────────────────┬─────────────────────┘
                                  │
                                  ▼
                     [Phase 1: Divergence (3 Nodes)]
               GPT Sol 6.1  •  Kimi K3  •  Grok 4.7
                                  │
                                  ▼
                   [Phase 2: Adversarial Critique]
                         Grok 4.7 (Red-Team)
                                  │
                                  ▼
                     [Phase 3: Master Synthesis]
                    Claude Sonnet 5.5 (Arbitrator)
                                  │
                                  ▼
                    [03_FINAL_SYNTHESIS_SONNET.md]
```

---

## 🚀 Quickstart

Everything in `agentic-quorum` is managed directly through `make`:

### 1. Verification
Verify that all 4 models respond in your Copilot CLI environment:

```bash
make verify
```

Output:
```text
🔍 Verifying Model & Reasoning Effort in Copilot CLI...
======================================================================
Checking Architect    : gpt-6.1-sol          [effort: high ] (OpenAI)... ✓ AVAILABLE
Checking Mechanist    : kimi-k3              [effort: high ] (Moonshot AI)... ✓ AVAILABLE
Checking Critic       : grok-4.7             [effort: high ] (xAI)... ✓ AVAILABLE
Checking Synthesizer  : claude-sonnet-5.5    [effort: high ] (Anthropic)... ✓ AVAILABLE
======================================================================
✅ All quorum nodes are active and reachable!
```

### 2. Standalone Gatekeeper Premise Audit
Audit a concept for architectural tunnel-vision in 10 seconds:

```bash
make audit TOPIC="End-to-End Automated Pipeline: OpenAPI v3 Spec to Native Crossplane Provider"
```

Output:
```text
🛑 [GATEKEEPER ALERT] Premise Tunnel-Vision Detected!

⚠️  WRIST-SLAP:
   You locked onto 'OpenAPI v3 → native Crossplane provider codegen' before asking 
   whether a native provider is the right artifact. A native provider is a Go controller 
   fleet, not a schema translation. Building that pipeline from scratch is the hard, 
   non-boring path the ecosystem already rejected for most APIs.

💡 INDUSTRY REALITY CHECK:
   95% of production Crossplane does not generate native providers from OpenAPI. 
   Official AWS/Azure/GCP coverage is Terraform schema → Upjet. Where no Terraform provider 
   exists, teams either generate a Terraform provider from OpenAPI and then run Upjet, 
   or compose existing providers.

🔀 VIABLE ALTERNATIVES:
   • Path A: Existing Terraform provider → Upjet
   • Path B: OpenAPI → generated Terraform provider → Upjet
   • Path C: Composition + Functions over existing providers
   • Path D: Narrow native Go provider only for edge-cases

📋 PROPOSED BROADENED AGENDA:
   "Objective trade-off: exposing an HTTP API as Crossplane managed resources — 
   Upjet-from-Terraform vs OpenAPI-to-Terraform-to-Upjet vs Composition/Functions vs 
   a narrowly scoped native provider..."
```

---

## 💻 Running Research via Make

### 1. General Research Topic
Run research on any architecture or distributed systems problem:

```bash
# Interactive Gatekeeper will audit your premise first, then launch the swarm
make research TOPIC="Zero-copy eBPF data plane vs DPDK in high-throughput network gateways"
```

### 2. Specialized Preset Shortcut
```bash
# Research OpenAPI to Crossplane with trade-offs evaluation
make research-crossplane

# Audit OpenAPI to Crossplane premise
make audit-crossplane
```

### 3. Advanced Flags via Make
```bash
# Run with automatic Gatekeeper broadening (no interactive prompt)
make research TOPIC="My Concept" GATEKEEPER=auto

# Bypass Gatekeeper
make research TOPIC="My Concept" GATEKEEPER=off

# Override reasoning effort level
make research TOPIC="My Concept" REASONING=max
```

### 4. Inspect Models & Presets
```bash
make models
make presets
```

---

## 📁 Artifacts Output Structure

Every run creates a timestamped folder inside `runs/`:

```text
runs/2026-10-24_23-15-00_openapi-to-crossplane/
├── 00_gatekeeper_audit.md             # Phase 0 premise audit & wrist-slap analysis
├── 00_topic.md                        # Query metadata, models & reasoning levels
├── 01_architect_gpt_sol.md            # Comparative architectural trade-offs & IR
├── 01_mechanist_kimi_k3.md            # Reconciler lifecycle & Go types
├── 01_critic_grok.md                  # Unhedged production failure modes
├── 02_adversarial_critique_grok.md    # Grok attack on Architect & Mechanist
├── 03_FINAL_SYNTHESIS_SONNET.md       # Master Architecture RFC
└── run_summary.json                   # Latency metrics & execution metadata
```

---

## ⚙️ Configuration (`quorum.json`)

```json
{
  "models": {
    "architect": "gpt-6.1-sol",
    "mechanist": "kimi-k3",
    "critic": "grok-4.7",
    "synthesizer": "claude-sonnet-5.5",
    "gatekeeper": "grok-4.7"
  },
  "gatekeeper": {
    "enabled": true,
    "mode": "interactive",
    "model": "grok-4.7"
  },
  "runner": {
    "cli_binary": "copilot",
    "default_flags": ["-s", "--no-color"],
    "default_reasoning_effort": "high",
    "timeout_seconds": 1200,
    "runs_dir": "runs"
  }
}
```

---

## 📄 License
Apache License 2.0. See [LICENSE](LICENSE) for details.
