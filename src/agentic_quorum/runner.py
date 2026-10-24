"""Copilot CLI subprocess runner."""

import asyncio
import os
import shutil
import sys
import time
from pathlib import Path
from typing import List, Optional, Tuple


class CopilotRunner:
    def __init__(
        self,
        cli_binary: str = "copilot",
        default_flags: Optional[List[str]] = None,
        default_reasoning_effort: str = "max",
        timeout_seconds: int = 600,
    ):
        self.cli_binary = cli_binary
        self.default_flags = default_flags if default_flags is not None else ["-s", "--no-color"]
        self.default_reasoning_effort = default_reasoning_effort
        self.timeout_seconds = timeout_seconds

        # Verify CLI executable exists
        resolved_bin = shutil.which(cli_binary)
        if not resolved_bin:
            raise FileNotFoundError(
                f"Binary '{cli_binary}' was not found in PATH. "
                "Ensure GitHub Copilot CLI is installed and accessible."
            )
        self.resolved_bin = resolved_bin

    async def execute(
        self,
        model: str,
        prompt: str,
        output_file: Optional[Path] = None,
        reasoning_effort: Optional[str] = None,
        extra_flags: Optional[List[str]] = None,
    ) -> Tuple[bool, str, float]:
        """
        Execute a prompt against Copilot CLI non-interactively using the specified model.
        Returns: (success: bool, output_text: str, duration_seconds: float)
        """
        flags = list(self.default_flags)
        if extra_flags:
            flags.extend(extra_flags)

        effort = reasoning_effort or self.default_reasoning_effort
        cmd = [self.resolved_bin] + flags + ["--model", model]
        if effort:
            cmd.extend(["--reasoning-effort", effort])
        cmd.extend(["-p", prompt])

        start_time = time.monotonic()
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            try:
                stdout_bytes, stderr_bytes = await asyncio.wait_for(
                    process.communicate(), timeout=self.timeout_seconds
                )
            except asyncio.TimeoutError:
                try:
                    process.kill()
                    await process.wait()
                except ProcessLookupError:
                    pass
                duration = time.monotonic() - start_time
                err_msg = f"Model execution timed out after {self.timeout_seconds}s"
                if output_file:
                    output_file.write_text(f"ERROR: {err_msg}\n", encoding="utf-8")
                return False, err_msg, duration

            duration = time.monotonic() - start_time
            stdout_str = stdout_bytes.decode("utf-8", errors="replace").strip()
            stderr_str = stderr_bytes.decode("utf-8", errors="replace").strip()

            if process.returncode != 0:
                err_detail = stderr_str or stdout_str or f"exit code {process.returncode}"
                if output_file:
                    output_file.write_text(f"ERROR: {err_detail}\n", encoding="utf-8")
                return False, err_detail, duration

            if output_file:
                output_file.parent.mkdir(parents=True, exist_ok=True)
                output_file.write_text(stdout_str, encoding="utf-8")

            return True, stdout_str, duration

        except Exception as e:
            duration = time.monotonic() - start_time
            err_msg = f"Subprocess exception: {e}"
            if output_file:
                output_file.write_text(f"ERROR: {err_msg}\n", encoding="utf-8")
            return False, err_msg, duration

    async def verify_model(self, model: str, reasoning_effort: str = "low") -> bool:
        """Quickly check if a model ID is available in Copilot CLI."""
        cmd = [
            self.resolved_bin,
            "-s",
            "--no-color",
            "--model",
            model,
            "--reasoning-effort",
            reasoning_effort,
            "-p",
            "echo 1",
        ]
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            _, stderr = await asyncio.wait_for(process.communicate(), timeout=15)
            if process.returncode == 0:
                return True
            err_text = stderr.decode("utf-8", errors="ignore")
            return "not available" not in err_text.lower()
        except Exception:
            return False
