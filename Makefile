# Lint and autofix for the plugin's markdown and JSON (see package.json).
# devbox provides node through direnv; npm installs the linters from
# package-lock.json, again only when the lock file changes.

INSTALLED := node_modules/.package-lock.json

# The hard cap: no line over ABSOLUTE_MAXIMUM_LINE_LENGTH (from .envrc),
# even ones lint exempts (tables, code spans, URLs). It skips files
# .gitattributes marks skip-absolute-line-length.
LINE_CAP_FILES := git ls-files -z -- ':(attr:!skip-absolute-line-length)'

.PHONY: lint fix node_modules

lint: $(INSTALLED)
	@npm run lint
	@$(LINE_CAP_FILES) | xargs -0 bin/validate_absolute_line_length

fix: $(INSTALLED)
	@npm run fix

node_modules: $(INSTALLED)

$(INSTALLED): package-lock.json
	npm ci
