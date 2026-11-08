// Compares what the plugin has with what Justin expects. Each assert
// method is one test's failure condition, and throws
// NameChangeNotApproved naming every change it found.

import { NameChangeNotApproved } from "./failures.mjs";

const RENAME_NOTE = "A rename fails twice: once as new, once as missing.";

// One kind of name, such as skills: the plugin's against Justin's list.
export class NamesCheck {
    #plugin;
    #expected;

    constructor(pluginNames, expectedNames) {
        this.#plugin = pluginNames;
        this.#expected = expectedNames;
    }

    // A name the plugin has that Justin's list doesn't.
    assertNoneUnexpected() {
        const isNew = (name) => !this.#expected.has(name);
        const added = this.#plugin.names.filter(isNew).sort();
        this.#rejectRenames(added.map((name) => this.#describeNew(name)));
    }

    // A name on Justin's list that the plugin doesn't have.
    assertNoneMissing() {
        const isMissing = (name) => !this.#plugin.has(name);
        const missing = this.#expected.names.filter(isMissing).sort();
        this.#rejectRenames(missing.map((name) => this.#describeMissing(name)));
    }

    #describeNew(name) {
        const { kind, fileOf } = this.#plugin;
        const list = this.#expected.file;
        return `New ${kind}: ${name} (${fileOf(name)}), not in ${list}`;
    }

    #describeMissing(name) {
        const { kind, fileOf } = this.#plugin;
        const list = this.#expected.file;
        const where = `no ${fileOf(name)}`;
        return `Missing ${kind}: ${name} (${where}), listed in ${list}`;
    }

    #rejectRenames(changes) {
        if (changes.length === 0) return;
        const lines = [...changes, RENAME_NOTE];
        throw new NameChangeNotApproved(lines, this.#expected.file);
    }
}

// plugin.json's fields against the values Justin expects, one at a time.
export class PluginJsonCheck {
    #plugin;
    #expected;

    constructor(pluginJson, expectedPluginJson) {
        this.#plugin = pluginJson;
        this.#expected = expectedPluginJson;
    }

    assertField(field) {
        const expected = JSON.stringify(this.#expected.get(field));
        const actual = JSON.stringify(this.#plugin.get(field));
        if (this.#plugin.has(field) && actual === expected) return;

        const change = this.#plugin.has(field)
            ? `${this.#plugin.path} has ${field} ${actual}, not ${expected}`
            : `${this.#plugin.path} has no ${field}; expected ${expected}`;
        throw new NameChangeNotApproved([change], this.#expected.file);
    }
}
