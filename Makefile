# Lint and autofix for the plugin's markdown and JSON (see package.json).
# devbox provides node through direnv; npm installs the linters from
# package-lock.json, again only when the lock file changes.

INSTALLED := node_modules/.package-lock.json

# The hard cap: no line over 145 columns, even ones lint exempts (tables,
# code spans, URLs). awk counts bytes, so it drops UTF-8 continuation
# bytes first, leaving one per character.
LINE_CAP := 145
LINE_CAP_SKIP := ':!:*.lock' ':!:package-lock.json'
# plugin.json's description is one JSON string, which can't be wrapped.
LINE_CAP_SKIP += ':!:.claude-plugin/plugin.json'
OVER_CAP = { s = $$0; gsub(/[\200-\277]/, "", s) } \
	length(s) > $(LINE_CAP) { print FILENAME ":" FNR ": " length(s); n++ } \
	END { exit n > 0 }

.PHONY: lint fix node_modules

lint: $(INSTALLED)
	@npm run lint
	@git ls-files -z -- $(LINE_CAP_SKIP) | \
		xargs -0 env LC_ALL=C awk '$(OVER_CAP)'

fix: $(INSTALLED)
	@npm run fix

node_modules: $(INSTALLED)

$(INSTALLED): package-lock.json
	npm ci
