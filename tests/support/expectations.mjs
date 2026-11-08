// What Justin expects the plugin's user-facing names to be. All of it
// lives in tests/expected/, one file per kind of name. Only he edits
// that folder; a local hook blocks every Claude session from it.

import { readFileSync } from "node:fs";
import { join } from "node:path";

const FOLDER = "tests/expected";
const COMMENT = "#";
const MANIFEST = ".claude-plugin/plugin.json";

// The folder as a whole: one property per file in it.
export class Expectations {
    #repo;

    constructor(repo) {
        this.#repo = repo;
    }

    get skills() {
        const locate = (name) => `skills/${name}/`;
        return new ExpectedNames(this.#read("skills.txt"), locate);
    }

    get agents() {
        const locate = (name) => `agents/${name}.md`;
        return new ExpectedNames(this.#read("agents.txt"), locate);
    }

    get manifest() {
        return new ExpectedManifest(this.#read("plugin.json"));
    }

    #read(name) {
        const file = `${FOLDER}/${name}`;
        return { file, text: readFileSync(join(this.#repo, file), "utf8") };
    }
}

// One list of names, such as skills.txt: one name per line, blank
// lines and # comments skipped. locate(name) gives the path in the
// repo where that name should exist, for the failure message.
export class ExpectedNames {
    #names;
    #locate;

    constructor({ file, text }, locate) {
        this.file = file;
        this.#names = parseNames(text);
        this.#locate = locate;
    }

    // Fails on a name the plugin has that this file doesn't list.
    assertNoneUnexpected(found) {
        const unexpected = found.filter((name) => !this.#names.has(name));
        const lines = unexpected.sort().map((name) => this.#unexpected(name));
        if (lines.length > 0) throw new NameChangeNotApproved(lines, this.file);
    }

    // Fails on a name this file lists that the plugin doesn't have.
    assertNoneMissing(found) {
        const present = new Set(found);
        const missing = [...this.#names].filter((name) => !present.has(name));
        const lines = missing.sort().map((name) => this.#missing(name));
        if (lines.length > 0) throw new NameChangeNotApproved(lines, this.file);
    }

    #unexpected(name) {
        return `${this.#locate(name)} is not in ${this.file}`;
    }

    #missing(name) {
        return `${this.file} lists ${name}; there is no ${this.#locate(name)}`;
    }
}

// plugin.json's fixed fields: only the keys listed are checked, so
// version and description change freely.
export class ExpectedManifest {
    #values;

    constructor({ file, text }) {
        this.file = file;
        this.#values = JSON.parse(text);
    }

    get fields() {
        return Object.entries(this.#values);
    }

    assertField(field, manifest) {
        const actual = JSON.stringify(manifest[field]);
        const expected = JSON.stringify(this.#values[field]);
        if (actual === expected) return;

        const line = `${MANIFEST} has ${field} ${actual}, not ${expected}`;
        throw new NameChangeNotApproved([line], this.file);
    }
}

// A user-facing name changed without Justin's yes. The message says
// what changed and what to do next; no stack trace, since the place
// that threw tells the reader nothing.
export class NameChangeNotApproved extends Error {
    constructor(changes, file) {
        super([...changes, "", ...nextSteps(file)].join("\n"));
        this.name = "NameChangeNotApproved";
        this.stack = `${this.name}: ${this.message}`;
    }
}

function nextSteps(file) {
    return [
        "User-facing names change only with Justin's explicit yes.",
        "  Didn't mean to change a name? Put it back.",
        "  Meant to? Ask Justin on the PR, and leave tests/expected/ alone.",
        `  With his yes, he updates ${file} himself.`,
    ];
}

function parseNames(text) {
    const lines = text.split("\n").map((line) => line.trim());
    return new Set(lines.filter((l) => l && !l.startsWith(COMMENT)));
}
