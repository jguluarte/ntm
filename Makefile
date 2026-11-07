# Lint and autofix for the plugin's markdown and JSON (see package.json).
# devbox provides node through direnv; npm installs the linters from
# package-lock.json, again only when the lock file changes.

INSTALLED := node_modules/.package-lock.json

# The line length settings, shared with direnv, which loads the same file.
include .env
export ABSOLUTE_MAXIMUM_LINE_LENGTH EXCLUDE_MAXIMUM_LINE_LENGTH_CHECK

.PHONY: lint fix node_modules

lint: $(INSTALLED)
	@npm run lint
	@bin/validate_absolute_line_length

fix: $(INSTALLED)
	@npm run fix

node_modules: $(INSTALLED)

$(INSTALLED): package-lock.json
	npm ci
