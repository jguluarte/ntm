
.PHONY: lint lint-markdown lint-yaml lint-python lint-absolute-line-length
.PHONY: lint-fix lint-fix-markdown test

LINT_FILES := $(shell git ls-files -- ':(attr:!skip-absolute-line-length)')
YAML_FILES := $(shell git ls-files -- '*.yml' '*.yaml')

TOO_LONG = length > $(ABSOLUTE_MAXIMUM_LINE_LENGTH)
REPORT = { print FILENAME; bad = 1; nextfile } END { exit bad }

lint: lint-markdown lint-yaml lint-python lint-absolute-line-length
	prettier --check .

lint-markdown:
	markdownlint-cli2

lint-yaml:
	yamllint --strict $(YAML_FILES)

lint-python:
	ruff check

lint-absolute-line-length:
	@awk '$(TOO_LONG) $(REPORT)' $(LINT_FILES)

lint-fix: lint-fix-markdown
	prettier --write .

lint-fix-markdown:
	markdownlint-cli2 --fix

test: export PYTHONPATH := scripts/picker:$(PYTHONPATH)
test:
	bats tests
	python3 -m unittest discover -s scripts/picker/test
