"""Command Line Interface for agentic-quorum."""

import argparse
import asyncio
import sys
from pathlib import Path
from typing import Optional

from agentic_quorum import __version__
from agentic_quorum.config import QuorumConfig
from agentic_quorum.engine import QuorumEngine
from agentic_quorum.prompts import PRESETS

REASONING_CHOICES = ["none", "minimal", "low", "medium", "high", "xhigh", "max"]


def cmd_research(args: argparse.Namespace) -> int:
    config = QuorumConfig.load(Path(args.config) if args.config else None)
    
    # Model overrides if passed
    if args.architect:
        config.models["architect"] = args.architect
    if args.mechanist:
        config.models["mechanist"] = args.mechanist
    if args.critic:
        config.models["critic"] = args.critic
    if args.synthesizer:
        config.models["synthesizer"] = args.synthesizer

    engine = QuorumEngine(config)
    output_path = Path(args.output) if args.output else None

    try:
        run_dir = asyncio.run(
            engine.run(
                args.topic,
                preset_name=args.preset,
                output_dir=output_path,
                reasoning_effort_override=args.reasoning_effort,
            )
        )
        print(f"\nTip: Explore the generated RFC and intermediate reports in:\n  open {run_dir}")
        return 0
    except KeyboardInterrupt:
        print("\n[!] Execution interrupted by user.")
        return 130
    except Exception as e:
        print(f"\n[!] Error during Quorum execution: {e}")
        return 1


def cmd_verify(args: argparse.Namespace) -> int:
    config = QuorumConfig.load(Path(args.config) if args.config else None)
    engine = QuorumEngine(config)

    print("\n🔍 Verifying Model & Reasoning Effort in Copilot CLI...")
    print("=" * 70)

    async def _check_all():
        checks = []
        for role, model in config.models.items():
            effort = config.get_reasoning_effort(role)
            info = config.roles.get(role)
            lab = f"({info.lab})" if info else ""
            print(f"Checking {role.capitalize():<12} : {model:<20} [effort: {effort:<5}] {lab}...", end=" ", flush=True)
            avail = await engine.runner.verify_model(model, reasoning_effort=effort)
            if avail:
                print("✓ AVAILABLE")
            else:
                print("✗ NOT AVAILABLE")
            checks.append((role, model, avail))
        return checks

    results = asyncio.run(_check_all())
    print("=" * 70)
    all_ok = all(r[2] for r in results)
    if all_ok:
        print("✅ All 4 quorum nodes are active and reachable with reasoning effort configured!")
        return 0
    else:
        print("⚠️ Some models failed verification. Check CLI permissions or flags.")
        return 1


def cmd_presets(args: argparse.Namespace) -> int:
    print("\n📋 Available Research Presets in agentic-quorum:")
    print("=" * 60)
    for name, p in PRESETS.items():
        print(f"• {name}")
        print(f"  Title: {p.get('title', 'N/A')}")
        print()
    print("Usage: agentic-quorum research \"<topic>\" --preset openapi-crossplane")
    return 0


def cmd_models(args: argparse.Namespace) -> int:
    config = QuorumConfig.load(Path(args.config) if args.config else None)
    print("\n🏛️  Configured Quorum Models, Roles & Reasoning Effort:")
    print("=" * 75)
    for role, model in config.models.items():
        info = config.roles.get(role)
        lab = info.lab if info else "Unknown"
        title = info.title if info else role.capitalize()
        focus = info.focus if info else ""
        effort = config.get_reasoning_effort(role)
        print(f"[{role.upper()}] -> {model}")
        print(f"  Lab             : {lab}")
        print(f"  Title           : {title}")
        print(f"  Reasoning Effort: {effort}")
        if focus:
            print(f"  Focus           : {focus}")
        print()
    print(f"Global Default Reasoning Effort: {config.runner.default_reasoning_effort}")
    print()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agentic-quorum",
        description="Multi-model consensus research engine orchestrating frontier AI models via Copilot CLI.",
    )
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-c", "--config", help="Path to custom quorum.json configuration")

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Command: research (or run)
    p_research = subparsers.add_parser("research", aliases=["run"], help="Run consensus research on a topic")
    p_research.add_argument("topic", help="The research topic or technical concept to explore")
    p_research.add_argument("-p", "--preset", help="Name of preset (e.g. openapi-crossplane)")
    p_research.add_argument("-o", "--output", help="Custom output directory for artifacts")
    p_research.add_argument(
        "-r",
        "--reasoning-effort",
        choices=REASONING_CHOICES,
        help="Override reasoning effort level for all models [none, minimal, low, medium, high, xhigh, max]",
    )
    p_research.add_argument("--architect", help="Override Architect model")
    p_research.add_argument("--mechanist", help="Override Mechanist model")
    p_research.add_argument("--critic", help="Override Critic model")
    p_research.add_argument("--synthesizer", help="Override Synthesizer model")
    p_research.set_defaults(func=cmd_research)

    # Command: verify
    p_verify = subparsers.add_parser("verify", help="Verify that all configured models respond via Copilot CLI")
    p_verify.set_defaults(func=cmd_verify)

    # Command: presets
    p_presets = subparsers.add_parser("presets", help="List available domain-specific research presets")
    p_presets.set_defaults(func=cmd_presets)

    # Command: models
    p_models = subparsers.add_parser("models", help="List configured models, labs, roles, and reasoning levels")
    p_models.set_defaults(func=cmd_models)

    return parser


def main() -> int:
    parser = build_parser()
    
    # If user runs `agentic-quorum "topic"`, treat it as `agentic-quorum research "topic"`
    args_list = sys.argv[1:]
    if args_list and args_list[0] not in ["research", "run", "verify", "presets", "models", "-h", "--help", "-v", "--version"]:
        args_list = ["research"] + args_list

    args = parser.parse_args(args_list)

    if not hasattr(args, "func"):
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
