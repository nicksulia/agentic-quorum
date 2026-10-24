.PHONY: help install verify models presets audit research research-crossplane audit-crossplane clean

PYTHON ?= python3
export PYTHONPATH := src:$(PYTHONPATH)

help:
	@echo "Agentic Quorum Commands:"
	@echo "  make research TOPIC=\"...\"     - Run research on any topic"
	@echo "                                   Optional: PRESET=... GATEKEEPER=interactive|auto|off REASONING=..."
	@echo "  make audit TOPIC=\"...\"        - Run Socratic Gatekeeper premise audit on a topic"
	@echo "  make research-crossplane      - Run research on OpenAPI to Crossplane using the preset"
	@echo "  make audit-crossplane         - Run Gatekeeper audit on OpenAPI to Crossplane"
	@echo "  make verify                   - Verify all frontier models in Copilot CLI"
	@echo "  make models                   - Display quorum model assignments & reasoning levels"
	@echo "  make presets                  - List available domain presets"
	@echo "  make install                  - Install agentic-quorum in editable mode"
	@echo "  make clean                    - Remove build artifacts and temporary files"

verify:
	$(PYTHON) -m agentic_quorum verify

models:
	$(PYTHON) -m agentic_quorum models

presets:
	$(PYTHON) -m agentic_quorum presets

audit:
	@if [ -z "$(TOPIC)" ]; then \
		echo "Error: TOPIC is required."; \
		echo "Usage: make audit TOPIC=\"Your concept or problem statement\""; \
		exit 1; \
	fi
	$(PYTHON) -m agentic_quorum audit "$(TOPIC)"

research:
	@if [ -z "$(TOPIC)" ]; then \
		echo "Error: TOPIC is required."; \
		echo "Usage: make research TOPIC=\"Your concept\" [PRESET=...] [GATEKEEPER=interactive|auto|off] [REASONING=high|max|...]"; \
		exit 1; \
	fi
	$(PYTHON) -m agentic_quorum research "$(TOPIC)" \
		$(if $(PRESET),--preset $(PRESET)) \
		$(if $(GATEKEEPER),--gatekeeper $(GATEKEEPER)) \
		$(if $(REASONING),--reasoning-effort $(REASONING))

audit-crossplane:
	$(PYTHON) -m agentic_quorum audit "End-to-End Automated Pipeline: OpenAPI v3 Spec to Crossplane Provider"

research-crossplane:
	$(PYTHON) -m agentic_quorum research "End-to-End Automated Pipeline: OpenAPI v3 Spec to Crossplane Provider" --preset openapi-crossplane

install:
	$(PYTHON) -m pip install -e .

clean:
	rm -rf build dist *.egg-info __pycache__ src/agentic_quorum/__pycache__
