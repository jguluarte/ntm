# Lint, autofix and tests for the plugin. devbox provides every tool
# through direnv: node for the linters, bats and jq for the tests.
#
# lint and fix check the markdown and JSON (see package.json); npm
# installs the linters from package-lock.json, again only when the lock
# file changes.

INSTALLED := node_modules/.package-lock.json

.PHONY: lint fix test node_modules

lint: $(INSTALLED)
	@npm run lint

fix: $(INSTALLED)
	@npm run fix

# Run the bats tests in tests/.
test:
	@bats tests

node_modules: $(INSTALLED)

$(INSTALLED): package-lock.json
	npm ci
