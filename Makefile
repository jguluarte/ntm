
.PHONY: lint lint-absolute-line-length lint-code-line-length lint-fix test

LINT_FILES := $(shell git ls-files -- ':(attr:!skip-absolute-line-length)')
YAML_FILES := $(shell git ls-files -- '*.yml' '*.yaml')
SHELL_SCRIPTS := scripts/picker/pick
CODE_FILES := $(SHELL_SCRIPTS) scripts/picker/pick.jq tests/picker.bats

TOO_LONG = length > $(ABSOLUTE_MAXIMUM_LINE_LENGTH)
TOO_LONG_FOR_CODE = length > $(MAXIMUM_LINE_LENGTH)
REPORT = { print FILENAME; bad = 1; nextfile } END { exit bad }

lint:
	prettier --check .
	markdownlint-cli2
	yamllint --strict $(YAML_FILES)
	shellcheck $(SHELL_SCRIPTS)
	$(MAKE) lint-absolute-line-length
	$(MAKE) lint-code-line-length

lint-absolute-line-length:
	@awk '$(TOO_LONG) $(REPORT)' $(LINT_FILES)

lint-code-line-length:
	@awk '$(TOO_LONG_FOR_CODE) $(REPORT)' $(CODE_FILES)

lint-fix:
	prettier --write .
	markdownlint-cli2 --fix

test:
	bats tests
