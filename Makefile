.PHONY: install test validate validate-tmdl validate-report report qa

PYTHON ?= python3
DOTNET ?= dotnet
REPORT_VALIDATOR := ./node_modules/.bin/powerbi-report-author
MODEL_DEFINITION := powerbi/OperationsKPI.SemanticModel/definition
REPORT_DEFINITION := powerbi/OperationsKPI.Report

install:
	npm ci
	$(DOTNET) restore --locked-mode tools/tmdl-validator/TmdlValidator.csproj

test:
	$(PYTHON) -m unittest discover -s tests -v

validate:
	$(PYTHON) scripts/validate_powerbi_assets.py

validate-tmdl:
	$(DOTNET) run --no-restore --project tools/tmdl-validator/TmdlValidator.csproj -- $(MODEL_DEFINITION)

validate-report:
	$(REPORT_VALIDATOR) validate $(REPORT_DEFINITION) --pretty

report:
	$(PYTHON) scripts/validate_powerbi_assets.py --write-report

qa: test validate validate-tmdl validate-report report
