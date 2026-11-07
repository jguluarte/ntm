// The hard cap: no line in a tracked file may run past 145 columns, even
// where Prettier and markdownlint allow it (tables, long code spans, URLs).
// The house rule is still 80; 145 is the limit nothing may exceed. Columns
// are counted in characters, not bytes, so an en dash is one. Files that
// .gitattributes marks linguist-generated (lock files) are skipped.

import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";

const MAX_COLUMNS = 145;
const GENERATED = "linguist-generated";
const SET = "set";
const TRUE = "true";
const NUL = "\0";

class TrackedFiles {
    static handWritten() {
        const paths = TrackedFiles.#git(["ls-files", "-z"]).split(NUL);
        const tracked = paths.filter(Boolean);
        const generated = TrackedFiles.#generated(tracked);

        return tracked.filter((path) => !generated.has(path));
    }

    // check-attr -z prints <path> NUL <attribute> NUL <value> NUL per path.
    static #generated(paths) {
        const args = ["check-attr", "-z", "--stdin", GENERATED];
        const fields = TrackedFiles.#git(args, paths.join(NUL)).split(NUL);
        const generated = new Set();

        for (let i = 0; i + 2 < fields.length; i += 3) {
            const value = fields[i + 2];

            if (value === SET || value === TRUE) generated.add(fields[i]);
        }

        return generated;
    }

    static #git(args, input) {
        return execFileSync("git", args, { input, encoding: "utf8" });
    }
}

class LineCap {
    constructor(maxColumns) {
        this.maxColumns = maxColumns;
    }

    violations(path) {
        const lines = readFileSync(path, "utf8").split(/\r?\n/);

        return lines
            .map((line, index) => ({
                path,
                line: index + 1,
                columns: [...line].length,
            }))
            .filter(({ columns }) => columns > this.maxColumns);
    }
}

const cap = new LineCap(MAX_COLUMNS);
const violations = TrackedFiles.handWritten().flatMap((path) =>
    cap.violations(path),
);

for (const { path, line, columns } of violations) {
    console.log(`${path}:${line}: ${columns}`);
}

if (violations.length > 0) {
    console.error(`${violations.length} lines over ${MAX_COLUMNS} columns.`);
    process.exit(1);
}
