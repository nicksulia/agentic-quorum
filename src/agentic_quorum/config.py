"""Configuration loader for agentic-quorum."""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class RoleConfig:
    model: str
    lab: str
    title: str
    focus: str
    reasoning_effort: str = "max"


@dataclass
class RunnerConfig:
    cli_binary: str = "copilot"
    default_flags: List[str] = field(default_factory=lambda: ["-s", "--no-color"])
    default_reasoning_effort: str = "max"
    timeout_seconds: int = 600
    runs_dir: str = "runs"


@dataclass
class QuorumConfig:
    models: Dict[str, str] = field(default_factory=lambda: {
        "architect": "gpt-6.1-sol",
        "mechanist": "kimi-k3",
        "critic": "grok-4.7",
        "synthesizer": "claude-sonnet-5.5"
    })
    roles: Dict[str, RoleConfig] = field(default_factory=dict)
    runner: RunnerConfig = field(default_factory=RunnerConfig)

    def get_reasoning_effort(self, role: str) -> str:
        """Get the reasoning effort level for a role, falling back to default."""
        if role in self.roles and self.roles[role].reasoning_effort:
            return self.roles[role].reasoning_effort
        return self.runner.default_reasoning_effort

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "QuorumConfig":
        """Load configuration from a JSON file, falling back to defaults."""
        search_paths = []
        if config_path:
            search_paths.append(Path(config_path))
        
        # Look in current working directory first, then package root
        search_paths.extend([
            Path.cwd() / "quorum.json",
            Path(__file__).resolve().parent.parent.parent / "quorum.json"
        ])

        for p in search_paths:
            if p.is_file():
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    
                    models = data.get("models", {})
                    runner_raw = data.get("runner", {})
                    default_effort = runner_raw.get("default_reasoning_effort", "max")

                    roles_raw = data.get("roles", {})
                    roles = {}
                    for k, v in roles_raw.items():
                        roles[k] = RoleConfig(
                            model=v.get("model", models.get(k, "")),
                            lab=v.get("lab", "Unknown"),
                            title=v.get("title", k.capitalize()),
                            focus=v.get("focus", ""),
                            reasoning_effort=v.get("reasoning_effort", default_effort),
                        )
                    
                    runner = RunnerConfig(
                        cli_binary=runner_raw.get("cli_binary", "copilot"),
                        default_flags=runner_raw.get("default_flags", ["-s", "--no-color"]),
                        default_reasoning_effort=default_effort,
                        timeout_seconds=runner_raw.get("timeout_seconds", 600),
                        runs_dir=runner_raw.get("runs_dir", "runs")
                    )
                    return cls(models=models, roles=roles, runner=runner)
                except Exception as e:
                    print(f"[Warning] Failed to parse config at {p}: {e}. Using defaults.")

        # Default fallback
        return cls()
