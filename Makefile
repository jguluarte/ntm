
.PHONY: lint lint-absolute-line-length lint-fix test

LINT_FILES := $(shell git ls-files -- ':(attr:!skip-absolute-line-length)')
YAML_FILES := $(shell git ls-files -- '*.yml' '*.yaml')

TOO_LONG = length > $(ABSOLUTE_MAXIMUM_LINE_LENGTH)
REPORT = { print FILENAME; bad = 1; nextfile } END { exit bad }

lint:
	prettier --check .
	markdownlint-cli2
	yamllint --strict $(YAML_FILES)
	ruff check
	$(MAKE) lint-absolute-line-length

lint-absolute-line-length:
	@awk '$(TOO_LONG) $(REPORT)' $(LINT_FILES)

lint-fix:
	prettier --write .
	markdownlint-cli2 --fix

test: export PYTHONPATH := scripts/picker:$(PYTHONPATH)
test:
	bats tests
	python3 -m unittest discover -s tests/picker
