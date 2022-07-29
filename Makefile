POETRY := $(shell command -v poetry 2> /dev/null)
INSTALL_STAMP := .install.stamp

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo ""
	@echo " install		install packages and prepare environment"
	@echo " clean		remove all temporary files"
	@echo " test		run all the tests"
	@echo " report		print coverage report"
	@echo " docs		create the docs"
	@echo " shell		open a Poetry shell"


install: $(INSTALL_STAMP)
$(INSTALL_STAMP): pyproject.toml
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	$(POETRY) install
	touch $(INSTALL_STAMP)

.PHONY: clean
clean:
	find . -type d -name "__pycache__" | xargs rm -rf {};
	rm -rf $(INSTALL_STAMP) .coverage .mypy_cache .pytest_cache
	rm -rf build
	rm -rf dist

.PHONY: test
test: $(INSTALL_STAMP)
	$(POETRY) run pytest --cov=src


.PHONY: report
report: $(INSTALL_STAMP)
	$(POETRY) run coverage report

.PHONY: docs
docs: $(INSTALL_STAMP)
	$(POETRY) run mkdocs build


.PHONY: shell
shell: $(INSTALL_STAMP)
	$(POETRY) shell