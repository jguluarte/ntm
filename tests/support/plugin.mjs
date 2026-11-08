// The plugin as it is in this repo: the names a user sees, and the file
// each one comes from. Everything is read once, when a Plugin is made.

import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const SKILLS = "skills";
const AGENTS = "agents";
const AGENT_SUFFIX = ".md";
const PLUGIN_JSON = ".claude-plugin/plugin.json";

export class Plugin {
    #root;

    constructor(root) {
        this.#root = root;
        this.skills = this.#readSkills();
        this.agents = this.#readAgents();
        this.pluginJson = this.#readPluginJson();
    }

    // A skill is a folder skills/<name>/.
    #readSkills() {
        const entries = this.#entries(SKILLS);
        const names = entries.filter((e) => e.isDirectory()).map((e) => e.name);
        return new PluginNames("skill", names, (name) => `${SKILLS}/${name}/`);
    }

    // An agent is a file agents/<name>.md.
    #readAgents() {
        const entries = this.#entries(AGENTS).filter((e) => e.isFile());
        const files = entries.filter((e) => e.name.endsWith(AGENT_SUFFIX));
        const names = files.map((e) => e.name.slice(0, -AGENT_SUFFIX.length));
        const fileOf = (name) => `${AGENTS}/${name}${AGENT_SUFFIX}`;
        return new PluginNames("agent", names, fileOf);
    }

    #readPluginJson() {
        const text = readFileSync(join(this.#root, PLUGIN_JSON), "utf8");
        return new PluginJson(PLUGIN_JSON, JSON.parse(text));
    }

    #entries(folder) {
        return readdirSync(join(this.#root, folder), { withFileTypes: true });
    }
}

// One kind of name the plugin has, such as its skills. fileOf(name) is
// where that name lives in the repo, or would live.
export class PluginNames {
    #names;

    constructor(kind, names, fileOf) {
        this.kind = kind;
        this.#names = new Set(names);
        this.fileOf = fileOf;
    }

    get names() {
        return [...this.#names];
    }

    has(name) {
        return this.#names.has(name);
    }
}

// .claude-plugin/plugin.json: where it is, and its values.
export class PluginJson {
    #values;

    constructor(path, values) {
        this.path = path;
        this.#values = values;
    }

    has(field) {
        return Object.hasOwn(this.#values, field);
    }

    get(field) {
        return this.#values[field];
    }
}
