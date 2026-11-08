# Lint and autofix for the plugin's markdown and JSON (see package.json).
# devbox provides node through direnv; npm installs the linters from
# package-lock.json, again only when the lock file changes.

INSTALLED := node_modules/.package-lock.json

.PHONY: lint fix test node_modules

lint: $(INSTALLED)
	@npm run lint

fix: $(INSTALLED)
	@npm run fix

# User-facing names match what Justin expects (tests/expected/). Node's
# own test runner, so nothing to install; spec output, because CI isn't
# a terminal and would get TAP otherwise.
test:
	@node --test --test-reporter=spec 'tests/*.test.mjs'

node_modules: $(INSTALLED)

$(INSTALLED): package-lock.json
	npm ci
