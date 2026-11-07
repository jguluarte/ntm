# Lint and autofix for the plugin's markdown and JSON (see package.json),
# plus the names check. devbox provides node through direnv; npm installs
# the linters from package-lock.json, again only when the lock file changes.

SHELL := bash
INSTALLED := node_modules/.package-lock.json

# The user-facing names in the repo: plugin.json's name and displayName, each
# skill folder that holds SKILL.md, each agent file without .md.
REPO_NAMES := { sed -nE 's/^    "(name|displayName)": "(.*)",?$$/\2/p' \
    .claude-plugin/plugin.json; ls skills/*/SKILL.md agents/*.md \
    | sed -E 's|^skills/(.*)/SKILL\.md$$|\1|; s|^agents/(.*)\.md$$|\1|'; } \
    | sort

# names.txt without its comments and blank lines.
LISTED_NAMES := grep -v -e '^\#' -e '^$$' names.txt | sort

NAMES_CHANGED := User-facing names changed. names.txt must change too, \
    and only Justin edits names.txt. Ask him.

.PHONY: lint fix names node_modules

lint: $(INSTALLED) names
	@npm run lint

fix: $(INSTALLED)
	@npm run fix

# Fails on any difference between the repo's names and names.txt.
names:
	@changes=$$(diff <($(LISTED_NAMES)) <($(REPO_NAMES)) \
	    | sed -n 's/^> /    added:   /p; s/^< /    removed: /p'); \
	[ -z "$$changes" ] || { echo "$(NAMES_CHANGED)"; echo "$$changes"; \
	    exit 1; } >&2

node_modules: $(INSTALLED)

$(INSTALLED): package-lock.json
	npm ci
