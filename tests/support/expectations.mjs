// What Justin expects the plugin's user-facing names to be. All of it
// lives in tests/expected/, one file per kind of name, and only he edits
// that folder. Everything is read once, when Expectations are made.

import { readFileSync } from "node:fs";
import { join } from "node:path";
import { BrokenExpectationFile } from "./failures.mjs";

const FOLDER = "tests/expected";
const COMMENT = "#";

// The folder as a whole: one property per file in it.
export class Expectations {
    #repo;

    constructor(repo) {
        this.#repo = repo;
        this.skills = new ExpectedNames(...this.#read("skills.txt"));
        this.agents = new ExpectedNames(...this.#read("agents.txt"));
        this.pluginJson = new ExpectedPluginJson(...this.#read("plugin.json"));
    }

    #read(name) {
        const file = `${FOLDER}/${name}`;
        try {
            return [file, readFileSync(join(this.#repo, file), "utf8")];
        } catch {
            throw new BrokenExpectationFile(file, "is missing or unreadable.");
        }
    }
}

// One list of names, such as skills.txt: one name per line, with blank
// lines and # comments skipped.
export class ExpectedNames {
    #names;

    constructor(file, text) {
        this.file = file;
        this.#names = ExpectedNames.parse(text);
    }

    static parse(text) {
        const lines = text.split("\n").map((line) => line.trim());
        return new Set(lines.filter((l) => l && !l.startsWith(COMMENT)));
    }

    get names() {
        return [...this.#names];
    }

    has(name) {
        return this.#names.has(name);
    }
}

// The plugin.json values Justin expects. Only the fields listed here are
// checked, so version and description change freely.
export class ExpectedPluginJson {
    #values;

    constructor(file, text) {
        this.file = file;
        this.#values = ExpectedPluginJson.parse(file, text);
    }

    static parse(file, text) {
        let values;
        try {
            values = JSON.parse(text);
        } catch (error) {
            const problem = `isn't valid JSON: ${error.message}`;
            throw new BrokenExpectationFile(file, problem);
        }

        const isObject = values && typeof values === "object";
        const fields = isObject && !Array.isArray(values) ? values : {};
        if (Object.keys(fields).length > 0) return fields;

        throw new BrokenExpectationFile(file, "lists no fields to check.");
    }

    get fields() {
        return Object.entries(this.#values);
    }

    get(field) {
        return this.#values[field];
    }
}
