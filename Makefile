
.PHONY: lint lint-absolute-line-length lint-fix test

LINT_FILES := $(shell git ls-files -- ':(attr:!skip-absolute-line-length)')

TOO_LONG = length > $(ABSOLUTE_MAXIMUM_LINE_LENGTH)
REPORT = { print FILENAME; bad = 1; nextfile } END { exit bad }

lint:
	prettier --check .
	markdownlint-cli2
	$(MAKE) lint-absolute-line-length

lint-absolute-line-length:
	@awk '$(TOO_LONG) $(REPORT)' $(LINT_FILES)

lint-fix:
	prettier --write .
	markdownlint-cli2 --fix

test:
	bats tests
