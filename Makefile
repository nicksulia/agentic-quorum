.PHONY: help install verify research-crossplane test models presets

PYTHON ?= python3
export PYTHONPATH := src:$(PYTHONPATH)

help:
	@echo "Agentic Quorum Makefile Commands:"
	@echo "  make verify               - Check availability of all 4 models in Copilot CLI"
	@echo "  make research-crossplane  - Run consensus research for OpenAPI to Crossplane"
	@echo "  make models               - Display quorum model assignments & roles"
	@echo "  make presets              - List available domain presets"
	@echo "  make install              - Install agentic-quorum in editable mode"

verify:
	$(PYTHON) -m agentic_quorum verify

models:
	$(PYTHON) -m agentic_quorum models

presets:
	$(PYTHON) -m agentic_quorum presets

research-crossplane:
	$(PYTHON) -m agentic_quorum research "End-to-End Automated Pipeline: OpenAPI v3 Spec to Native Crossplane Provider" --preset openapi-crossplane

install:
	$(PYTHON) -m pip install -e .
