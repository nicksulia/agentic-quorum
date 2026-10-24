"""Core execution engine for agentic-quorum research pipeline."""

import asyncio
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from agentic_quorum.config import QuorumConfig
from agentic_quorum.prompts import (
    GENERAL_ARCHITECT_PROMPT,
    GENERAL_MECHANIST_PROMPT,
    GENERAL_CRITIC_PROMPT,
    GENERAL_ADVERSARIAL_CRITIQUE_PROMPT,
    GENERAL_SYNTHESIS_PROMPT,
    PRESETS,
)
from agentic_quorum.runner import CopilotRunner


def slugify(text: str) -> str:
    """Generate a filesystem-safe slug from a string."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:40].strip("-") or "research"


class QuorumEngine:
    def __init__(self, config: Optional[QuorumConfig] = None):
        self.config = config or QuorumConfig.load()
        self.runner = CopilotRunner(
            cli_binary=self.config.runner.cli_binary,
            default_flags=self.config.runner.default_flags,
            default_reasoning_effort=self.config.runner.default_reasoning_effort,
            timeout_seconds=self.config.runner.timeout_seconds,
        )

    def _prepare_run_dir(self, topic: str) -> Path:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        slug = slugify(topic)
        base_dir = Path(self.config.runner.runs_dir)
        run_dir = base_dir / f"{timestamp}_{slug}"
        run_dir.mkdir(parents=True, exist_ok=True)
        return run_dir

    def _resolve_prompts(self, topic: str, preset_name: Optional[str] = None) -> Dict[str, str]:
        if preset_name and preset_name in PRESETS:
            preset = PRESETS[preset_name]
            return {
                "architect": preset["architect"],
                "mechanist": preset["mechanist"],
                "critic": preset["critic"],
                "adversarial": preset["adversarial"],
                "synthesizer": preset["synthesizer"],
            }
        
        return {
            "architect": GENERAL_ARCHITECT_PROMPT.format(topic=topic),
            "mechanist": GENERAL_MECHANIST_PROMPT.format(topic=topic),
            "critic": GENERAL_CRITIC_PROMPT.format(topic=topic),
            "adversarial": GENERAL_ADVERSARIAL_CRITIQUE_PROMPT,
            "synthesizer": GENERAL_SYNTHESIS_PROMPT,
        }

    async def run(
        self,
        topic: str,
        preset_name: Optional[str] = None,
        output_dir: Optional[Path] = None,
        reasoning_effort_override: Optional[str] = None,
    ) -> Path:
        """
        Execute the full 3-phase Quorum consensus pipeline.
        Returns the path to the completed run directory.
        """
        run_dir = output_dir or self._prepare_run_dir(topic)
        prompts = self._resolve_prompts(topic, preset_name)

        models = self.config.models
        m_architect = models["architect"]
        m_mechanist = models["mechanist"]
        m_critic = models["critic"]
        m_synthesizer = models["synthesizer"]

        # Resolve reasoning effort levels
        r_arch = reasoning_effort_override or self.config.get_reasoning_effort("architect")
        r_mech = reasoning_effort_override or self.config.get_reasoning_effort("mechanist")
        r_crit = reasoning_effort_override or self.config.get_reasoning_effort("critic")
        r_syn = reasoning_effort_override or self.config.get_reasoning_effort("synthesizer")

        # Write topic overview
        (run_dir / "00_topic.md").write_text(
            f"# Research Topic\n\n**Topic:** {topic}\n"
            f"**Preset:** {preset_name or 'None'}\n"
            f"**Timestamp:** {datetime.now().isoformat()}\n"
            f"**Nodes & Reasoning Levels:**\n"
            f"- Architect: `{m_architect}` (OpenAI) [reasoning: `{r_arch}`]\n"
            f"- Mechanist: `{m_mechanist}` (Moonshot AI) [reasoning: `{r_mech}`]\n"
            f"- Critic: `{m_critic}` (xAI) [reasoning: `{r_crit}`]\n"
            f"- Synthesizer: `{m_synthesizer}` (Anthropic) [reasoning: `{r_syn}`]\n",
            encoding="utf-8",
        )

        print(f"\n" + "=" * 70)
        print(f"🚀 AGENTIC QUORUM :: STARTING RESEARCH")
        print(f"   Topic  : {topic}")
        if preset_name:
            print(f"   Preset : {preset_name}")
        print(f"   Output : {run_dir.resolve()}")
        print("=" * 70)

        summary_metrics: Dict[str, Any] = {
            "topic": topic,
            "preset": preset_name,
            "start_time": datetime.now().isoformat(),
            "models": models,
            "reasoning_levels": {
                "architect": r_arch,
                "mechanist": r_mech,
                "critic": r_crit,
                "synthesizer": r_syn,
            },
            "phases": {},
        }

        # ----------------------------------------------------------------------
        # PHASE 1: DIVERGENT PARALLEL EXPLORATION
        # ----------------------------------------------------------------------
        print(f"\n[Phase 1/3] 🌐 Divergent Parallel Exploration (3 Models)")
        print(f"  ├─ [Architect]   {m_architect:<20} [reasoning: {r_arch}]")
        print(f"  ├─ [Mechanist]   {m_mechanist:<20} [reasoning: {r_mech}]")
        print(f"  └─ [Critic]      {m_critic:<20} [reasoning: {r_crit}]")

        f_architect = run_dir / "01_architect_gpt_sol.md"
        f_mechanist = run_dir / "01_mechanist_kimi_k3.md"
        f_critic = run_dir / "01_critic_grok.md"

        p1_start = time.monotonic()
        task_arch = self.runner.execute(
            m_architect, prompts["architect"], f_architect, reasoning_effort=r_arch
        )
        task_mech = self.runner.execute(
            m_mechanist, prompts["mechanist"], f_mechanist, reasoning_effort=r_mech
        )
        task_crit = self.runner.execute(
            m_critic, prompts["critic"], f_critic, reasoning_effort=r_crit
        )

        results = await asyncio.gather(task_arch, task_mech, task_crit)
        p1_duration = time.monotonic() - p1_start

        (s_arch, out_arch, d_arch), (s_mech, out_mech, d_mech), (s_crit, out_crit, d_crit) = results

        print(f"  ├─ Architect : {'✓ OK' if s_arch else '✗ FAILED'} ({d_arch:.1f}s)")
        print(f"  ├─ Mechanist : {'✓ OK' if s_mech else '✗ FAILED'} ({d_mech:.1f}s)")
        print(f"  └─ Critic    : {'✓ OK' if s_crit else '✗ FAILED'} ({d_crit:.1f}s)")
        print(f"  ↳ Phase 1 complete in {p1_duration:.1f}s")

        summary_metrics["phases"]["phase_1_divergence"] = {
            "duration": p1_duration,
            "architect": {"success": s_arch, "duration": d_arch, "file": f_architect.name},
            "mechanist": {"success": s_mech, "duration": d_mech, "file": f_mechanist.name},
            "critic": {"success": s_crit, "duration": d_crit, "file": f_critic.name},
        }

        # ----------------------------------------------------------------------
        # PHASE 2: ADVERSARIAL CROSS-CRITIQUE (RED-TEAM ATTACK)
        # ----------------------------------------------------------------------
        print(f"\n[Phase 2/3] ⚔️  Adversarial Cross-Critique & Stress-Testing")
        print(f"  └─ [Red-Team]    {m_critic:<20} [reasoning: {r_crit}] attacking drafts...")

        f_critique = run_dir / "02_adversarial_critique_grok.md"
        adv_prompt = prompts["adversarial"].format(
            topic=topic,
            architect_draft=out_arch,
            mechanist_draft=out_mech,
        )

        p2_start = time.monotonic()
        s_adv, out_adv, d_adv = await self.runner.execute(
            m_critic, adv_prompt, f_critique, reasoning_effort=r_crit
        )
        p2_duration = time.monotonic() - p2_start

        print(f"  └─ Red-Team  : {'✓ OK' if s_adv else '✗ FAILED'} ({d_adv:.1f}s)")
        print(f"  ↳ Phase 2 complete in {p2_duration:.1f}s")

        summary_metrics["phases"]["phase_2_critique"] = {
            "duration": p2_duration,
            "red_team": {"success": s_adv, "duration": d_adv, "file": f_critique.name},
        }

        # ----------------------------------------------------------------------
        # PHASE 3: CONVERGENCE & MASTER SYNTHESIS
        # ----------------------------------------------------------------------
        print(f"\n[Phase 3/3] 🏛️  Convergence & Master Synthesis")
        print(f"  └─ [Arbitrator]  {m_synthesizer:<20} [reasoning: {r_syn}] creating Master RFC...")

        f_final = run_dir / "03_FINAL_SYNTHESIS_SONNET.md"
        syn_prompt = prompts["synthesizer"].format(
            topic=topic,
            architect_draft=out_arch,
            mechanist_draft=out_mech,
            critic_draft=out_crit,
            adversarial_critique=out_adv,
        )

        p3_start = time.monotonic()
        s_syn, out_syn, d_syn = await self.runner.execute(
            m_synthesizer, syn_prompt, f_final, reasoning_effort=r_syn
        )
        p3_duration = time.monotonic() - p3_start

        print(f"  └─ Master RFC: {'✓ OK' if s_syn else '✗ FAILED'} ({d_syn:.1f}s)")
        print(f"  ↳ Phase 3 complete in {p3_duration:.1f}s")

        summary_metrics["phases"]["phase_3_synthesis"] = {
            "duration": p3_duration,
            "synthesizer": {"success": s_syn, "duration": d_syn, "file": f_final.name},
        }

        total_time = p1_duration + p2_duration + p3_duration
        summary_metrics["end_time"] = datetime.now().isoformat()
        summary_metrics["total_duration"] = total_time

        # Save summary JSON
        (run_dir / "run_summary.json").write_text(
            json.dumps(summary_metrics, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        print("\n" + "=" * 70)
        print(f"✅ QUORUM CONSENSUS REACHED (Total time: {total_time:.1f}s)")
        print(f"   Final Master RFC -> {f_final.resolve()}")
        print("=" * 70)

        return run_dir
