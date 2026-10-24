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
    reasoning_effort: str = "high"


@dataclass
class GatekeeperConfig:
    enabled: bool = True
    mode: str = "interactive"  # "interactive", "auto", "off"
    model: str = "grok-4.7"


@dataclass
class RunnerConfig:
    cli_binary: str = "copilot"
    default_flags: List[str] = field(default_factory=lambda: ["-s", "--no-color"])
    default_reasoning_effort: str = "high"
    timeout_seconds: int = 1200
    runs_dir: str = "runs"


@dataclass
class QuorumConfig:
    models: Dict[str, str] = field(default_factory=lambda: {
        "architect": "gpt-6.1-sol",
        "mechanist": "kimi-k3",
        "critic": "grok-4.7",
        "synthesizer": "claude-sonnet-5.5",
        "gatekeeper": "grok-4.7"
    })
    roles: Dict[str, RoleConfig] = field(default_factory=dict)
    gatekeeper: GatekeeperConfig = field(default_factory=GatekeeperConfig)
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
                    default_effort = runner_raw.get("default_reasoning_effort", "high")

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

                    gk_raw = data.get("gatekeeper", {})
                    gatekeeper = GatekeeperConfig(
                        enabled=gk_raw.get("enabled", True),
                        mode=gk_raw.get("mode", "interactive"),
                        model=gk_raw.get("model", models.get("gatekeeper", "grok-4.7"))
                    )
                    
                    runner = RunnerConfig(
                        cli_binary=runner_raw.get("cli_binary", "copilot"),
                        default_flags=runner_raw.get("default_flags", ["-s", "--no-color"]),
                        default_reasoning_effort=default_effort,
                        timeout_seconds=runner_raw.get("timeout_seconds", 1200),
                        runs_dir=runner_raw.get("runs_dir", "runs")
                    )
                    return cls(models=models, roles=roles, gatekeeper=gatekeeper, runner=runner)
                except Exception as e:
                    print(f"[Warning] Failed to parse config at {p}: {e}. Using defaults.")

        # Default fallback
        return cls()
