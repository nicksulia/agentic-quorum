# 🏛️ agentic-quorum

> **Multi-model consensus research engine.** Heterogeneous frontier models meeting for peer-reviewed, verified technical truth.

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Orchestrator](https://img.shields.io/badge/orchestrator-GitHub%20Copilot%20CLI-black.svg)](https://github.com/features/copilot)

`agentic-quorum` eliminates single-model cognitive bias, corporate safety blind spots, and hallucinations by orchestrating a distributed council of four leading frontier AI models from different research labs across a **three-phase consensus protocol** with configurable **reasoning effort levels** (`none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max`).

---

## 👥 The Quorum Council ("The Big Four")

Each model represents a distinct training paradigm, dataset heritage, and epistemic role:

| Node | Model Identifier | Frontier Lab | Specialized Role | Reasoning Effort | Primary Focus |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Architect** | `gpt-6.1-sol` | **OpenAI** | Systems Architect & Planner | `xhigh` | Pipeline decomposition, Intermediate Representation (IR), formal structures, and lifecycle workflows. |
| **Mechanist** | `kimi-k3` | **Moonshot AI** | Deep Runtime & Mechanics | `max` | State machines, Kubernetes CRD structural schema limits, async `202 Accepted` polling, and Go type safety. |
| **Critic** | `grok-4.7` | **xAI** | Chaos Engineer & Red-Team | `xhigh` | Production failure modes, drift detection loops, target API rate-limits (HTTP 429), and unhedged stress-testing. |
| **Synthesizer** | `claude-sonnet-5.5` | **Anthropic** | Chief Synthesizer & Arbitrator | `max` | Epistemic arbitration, resolving disagreements, mapping consensus vs divergence, and compiling the master RFC. |

---

## 🔄 The 3-Phase Consensus Protocol

```
                        [Technical Subject / Concept]
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        ▼                             ▼                             ▼
  [Phase 1: Divergence]      [Phase 1: Divergence]      [Phase 1: Divergence]
  GPT Sol 6.1 (effort: xhigh)  Kimi K3 (effort: max)    Grok 4.7 (effort: xhigh)
     Systems Architecture      Deep Runtime Mechanics       Initial Stress-Test
        │                             │                             │
   [Draft 01: Arch]              [Draft 01: Mech]              [Draft 01: Chaos]
        └─────────────────────────────┬─────────────────────────────┘
                                      │
                                      ▼
                        [Phase 2: Adversarial Audit]
                         Grok 4.7 (effort: xhigh)
                     Merciless attack on Drafts 01A & 01B
                                      │
                                [Audit Report]
                                      │
                                      ▼
                        [Phase 3: Master Synthesis]
                      Claude Sonnet 5.5 (effort: max)
                     Reconciles disputes & creates Master RFC
                                      │
                                      ▼
                       [03_FINAL_SYNTHESIS_SONNET.md]
```

### 1. Phase 1: Blind Divergent Exploration
All three exploration models receive identical baseline directives with deep reasoning enabled, executing in parallel without seeing each other's outputs to prevent anchor bias and groupthink.

### 2. Phase 2: Adversarial Cross-Critique
The Red-Team auditor (`grok-4.7`) is fed the drafts from the Architect and Mechanist with the explicit instruction to expose naive optimism, fragile assumptions, and production failure modes.

### 3. Phase 3: Epistemic Convergence & Master Synthesis
The Synthesizer (`claude-sonnet-5.5` with `effort: max`) reviews all three independent drafts plus the adversarial critique to produce an authoritative **Master Architecture Document (RFC)**:
- Core consensus points.
- Resolution of disputed attack vectors.
- Concrete data contracts and state machines.
- Phased implementation roadmap.

---

## 🚀 Quickstart

### Prerequisites
- Python 3.10+
- [GitHub Copilot CLI](https://github.com/features/copilot) installed and authenticated (`copilot --version`).

### Verification
Verify that all 4 models respond with their configured reasoning levels:

```bash
make verify
# or
python3 -m agentic_quorum verify
```

Output:
```text
🔍 Verifying Model & Reasoning Effort in Copilot CLI...
======================================================================
Checking Architect    : gpt-6.1-sol          [effort: xhigh] (OpenAI)... ✓ AVAILABLE
Checking Mechanist    : kimi-k3              [effort: max  ] (Moonshot AI)... ✓ AVAILABLE
Checking Critic       : grok-4.7             [effort: xhigh] (xAI)... ✓ AVAILABLE
Checking Synthesizer  : claude-sonnet-5.5    [effort: max  ] (Anthropic)... ✓ AVAILABLE
======================================================================
✅ All 4 quorum nodes are active and reachable with reasoning effort configured!
```

---

## 💻 Usage

### 1. General Concept Research
Explore any complex concept or distributed systems architecture:

```bash
# Direct execution (Zero external dependencies)
PYTHONPATH=src python3 -m agentic_quorum "High-throughput Paxos vs Raft in low-latency RDMA clusters"
```

### 2. Tuning Reasoning Effort via CLI
Override reasoning effort globally on the fly:

```bash
# Force maximum reasoning across all models
PYTHONPATH=src python3 -m agentic_quorum "Zero-copy eBPF data plane" --reasoning-effort max
```

### 3. Specialized Presets (e.g., OpenAPI to Crossplane)
`agentic-quorum` includes battle-tested domain presets:

```bash
# Run the OpenAPI-to-Crossplane Provider research
make research-crossplane
# or
PYTHONPATH=src python3 -m agentic_quorum research \
  "End-to-End Automated Pipeline: OpenAPI v3 to Native Crossplane Provider" \
  --preset openapi-crossplane
```

### 4. Inspect Presets, Models & Reasoning Levels
```bash
python3 -m agentic_quorum presets
python3 -m agentic_quorum models
```

---

## 📁 Artifacts Output Structure

Every run creates a timestamped folder inside `runs/`:

```text
runs/2026-10-24_22-15-00_openapi-to-crossplane/
├── 00_topic.md                        # Query metadata, models & reasoning levels
├── 01_architect_gpt_sol.md            # Pipeline decomposition & IR schema
├── 01_mechanist_kimi_k3.md            # Reconciler lifecycle & Go types
├── 01_critic_grok.md                  # Unhedged production failure modes
├── 02_adversarial_critique_grok.md    # Grok attack on Architect & Mechanist
├── 03_FINAL_SYNTHESIS_SONNET.md       # Master Architecture RFC
└── run_summary.json                   # Latency metrics & execution metadata
```

---

## ⚙️ Configuration (`quorum.json`)

Customize model IDs, reasoning effort levels, prompts, and CLI options directly in `quorum.json`:

```json
{
  "models": {
    "architect": "gpt-6.1-sol",
    "mechanist": "kimi-k3",
    "critic": "grok-4.7",
    "synthesizer": "claude-sonnet-5.5"
  },
  "roles": {
    "architect": {
      "model": "gpt-6.1-sol",
      "reasoning_effort": "xhigh"
    },
    "mechanist": {
      "model": "kimi-k3",
      "reasoning_effort": "max"
    },
    "critic": {
      "model": "grok-4.7",
      "reasoning_effort": "xhigh"
    },
    "synthesizer": {
      "model": "claude-sonnet-5.5",
      "reasoning_effort": "max"
    }
  },
  "runner": {
    "cli_binary": "copilot",
    "default_flags": ["-s", "--no-color"],
    "default_reasoning_effort": "max",
    "timeout_seconds": 600,
    "runs_dir": "runs"
  }
}
```

---

## 📄 License
Apache License 2.0. See [LICENSE](LICENSE) for details.
