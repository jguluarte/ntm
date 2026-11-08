# Lint and autofix for the plugin's markdown and JSON. devbox provides
# prettier and markdownlint-cli2 through direnv.

# The hard cap: no line over ABSOLUTE_MAXIMUM_LINE_LENGTH (from .envrc),
# even ones lint exempts (tables, code spans, URLs). It skips files
# .gitattributes marks skip-absolute-line-length.
LINE_CAP_FILES := git ls-files -z -- ':(attr:!skip-absolute-line-length)'

.PHONY: lint fix

lint:
	@prettier --check .
	@markdownlint-cli2
	@$(LINE_CAP_FILES) | xargs -0 bin/validate_absolute_line_length

fix:
	@prettier --write .
	@markdownlint-cli2 --fix
