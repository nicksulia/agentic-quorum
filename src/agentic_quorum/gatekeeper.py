"""Phase 0: Socratic Gatekeeper & Premise Auditor.

Slaps the user on the wrist when they suffer from premature solution-locking,
Not-Invented-Here (NIH) syndrome, or the XY-Problem.
"""

import asyncio
import json
import re
import sys
from dataclasses import dataclass, field
from typing import List, Optional

from agentic_quorum.runner import CopilotRunner


GATEKEEPER_PROMPT = """
You are the Socratic Gatekeeper and Premise Auditor in an elite technical architecture council.
Your job is to SLAP THE USER ON THE WRIST if they make foolish, premature, or tunnel-visioned architectural assumptions before doing research.

The user wants to research the following topic:
"{topic}"

ANALYZE THIS TOPIC WITH ZERO COMPLIANCE BIAS:
1. Premature Solution-Locking / XY-Problem:
   Is the user asking HOW to build a specific, complex, custom solution (X) when their actual goal is (Y), and X is an anti-pattern or unnecessary?
2. Not-Invented-Here (NIH) Syndrome:
   Is the user attempting to write a custom tool/generator from scratch when a de-facto industry standard or bridge already exists (e.g., trying to write a custom Native Crossplane generator from scratch while ignoring OpenAPI -> Terraform -> Upjet)?
3. The "Boring Solution" Reality Check:
   How does 95% of the production cloud-native ecosystem actually solve this problem pragmatically?

OUTPUT REQUIREMENTS:
You MUST respond with valid JSON enclosed within a ```json code block with the following schema:
```json
{{
  "premature_locking": true,
  "wrist_slap": "Direct, blunt explanation of why the user's premise is flawed or prematurely locked into a sub-optimal path (e.g. locked into custom Go native codegen vs Terraform/Upjet).",
  "industry_standard": "How 95% of the industry actually solves this in production using existing boring tech / bridges.",
  "viable_alternatives": [
    "Path A: ...",
    "Path B: ...",
    "Path C: ..."
  ],
  "broadened_topic": "The de-biased, open research topic that compares the alternatives rather than blindly implementing a single doomed path."
}}
```
Set "premature_locking": true if the user's topic prescribes a narrow, complex, or questionable implementation path instead of asking for an objective architectural trade-off evaluation.
"""


@dataclass
class GatekeeperVerdict:
    is_anchored: bool
    wrist_slap: str
    industry_standard: str
    viable_alternatives: List[str] = field(default_factory=list)
    broadened_topic: str = ""
    raw_output: str = ""


class Gatekeeper:
    def __init__(self, runner: CopilotRunner, model: str = "grok-4.7"):
        self.runner = runner
        self.model = model

    async def audit_topic(self, topic: str) -> GatekeeperVerdict:
        """Run Socratic premise audit on the user's topic."""
        prompt = GATEKEEPER_PROMPT.format(topic=topic)
        success, output, _ = await self.runner.execute(
            model=self.model,
            prompt=prompt,
            reasoning_effort="low",  # fast turnaround
        )

        if not success:
            return GatekeeperVerdict(
                is_anchored=False,
                wrist_slap="",
                industry_standard="",
                raw_output=output,
            )

        try:
            json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", output, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(1))
            else:
                data = json.loads(output.strip())

            # Detect premature locking / tunnel vision
            is_locked = bool(
                data.get("premature_locking")
                or data.get("is_anchored")
                or (data.get("wrist_slap") and len(data.get("wrist_slap", "")) > 40)
            )

            return GatekeeperVerdict(
                is_anchored=is_locked,
                wrist_slap=data.get("wrist_slap", ""),
                industry_standard=data.get("industry_standard", ""),
                viable_alternatives=data.get("viable_alternatives", []),
                broadened_topic=data.get("broadened_topic", topic),
                raw_output=output,
            )
        except Exception:
            anchored = any(k in output.lower() for k in ["xy problem", "nih", "upjet", "premature", "tunnel vision"])
            return GatekeeperVerdict(
                is_anchored=anchored,
                wrist_slap=output[:400],
                industry_standard="",
                broadened_topic=topic,
                raw_output=output,
            )

    def interact(self, verdict: GatekeeperVerdict, original_topic: str) -> str:
        """
        Display the Gatekeeper wrist-slap to the user in the terminal and prompt for direction.
        Returns the chosen topic (either broadened or original).
        """
        if not verdict.is_anchored:
            print("✓ [Gatekeeper] Topic premise verified: No severe anchoring detected.")
            return original_topic

        print("\n" + "=" * 75)
        print("🛑 [GATEKEEPER ALERT] Premise Tunnel-Vision / XY-Problem Detected!")
        print("=" * 75)
        print(f"\nOriginal Topic: \"{original_topic}\"\n")
        print("⚠️  WRIST-SLAP:")
        print(f"   {verdict.wrist_slap}\n")
        
        if verdict.industry_standard:
            print("💡 INDUSTRY REALITY CHECK:")
            print(f"   {verdict.industry_standard}\n")

        if verdict.viable_alternatives:
            print("🔀 VIABLE ARCHITECTURAL PATHS TO EVALUATE:")
            for alt in verdict.viable_alternatives:
                print(f"   • {alt}")
            print()

        print("📋 PROPOSED BROADENED AGENDA:")
        print(f"   \"{verdict.broadened_topic}\"\n")

        print("-" * 75)
        print("HOW DO YOU WISH TO PROCEED?")
        print("  [1] (Recommended) Broaden Scope: Evaluate all architectural trade-offs")
        print("  [2] Force Original: I know what I'm doing, strictly research original topic")
        print("  [3] Abort execution")
        print("-" * 75)

        while True:
            try:
                choice = input("\nEnter choice [1/2/3] (default 1): ").strip() or "1"
                if choice == "1":
                    print(f"\n✓ Scope broadened to: \"{verdict.broadened_topic}\"")
                    return verdict.broadened_topic
                elif choice == "2":
                    print(f"\n⚠️ Proceeding with original strict topic: \"{original_topic}\"")
                    return original_topic
                elif choice == "3":
                    print("\n[!] Execution aborted by user.")
                    sys.exit(0)
                else:
                    print("Invalid option. Please enter 1, 2, or 3.")
            except (KeyboardInterrupt, EOFError):
                print("\n[!] Execution aborted.")
                sys.exit(0)
