// The plugin as it is in this repo: the names a user sees, and the file
// each one comes from. Everything is read once, when a Plugin is made.

import { existsSync, readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const SKILLS = "skills";
const SKILL_FILE = "SKILL.md";
const AGENTS = "agents";
const AGENT_SUFFIX = ".md";
const PLUGIN_JSON = ".claude-plugin/plugin.json";

// The frontmatter block at the top of a skill or agent file, and the
// name: line inside it.
const FRONTMATTER = /^---\r?\n([\s\S]*?)\r?\n---/;
const NAME_LINE = /^name:\s*(.*?)\s*$/m;

export class Plugin {
    #root;

    constructor(root) {
        this.#root = root;
        this.skills = this.#readSkills();
        this.agents = this.#readAgents();
        this.pluginJson = this.#readPluginJson();
    }

    // A skill is a folder skills/<name>/ with a SKILL.md in it.
    #readSkills() {
        const fileOf = (name) => `${SKILLS}/${name}/${SKILL_FILE}`;
        const isSkill = (name) => existsSync(join(this.#root, fileOf(name)));
        const names = readdirSync(join(this.#root, SKILLS)).filter(isSkill);
        return this.#names("skill", names, fileOf);
    }

    // An agent is a file agents/<name>.md.
    #readAgents() {
        const fileOf = (name) => `${AGENTS}/${name}${AGENT_SUFFIX}`;
        const files = readdirSync(join(this.#root, AGENTS));
        const agents = files.filter((file) => file.endsWith(AGENT_SUFFIX));
        const names = agents.map((file) => file.slice(0, -AGENT_SUFFIX.length));
        return this.#names("agent", names, fileOf);
    }

    // Each name with the name: line its file declares.
    #names(kind, names, fileOf) {
        const declared = new Map();
        for (const name of names) {
            const text = this.#text(fileOf(name));
            declared.set(name, declaredName(text));
        }
        return new PluginNames(kind, declared, fileOf);
    }

    #readPluginJson() {
        return new PluginJson(PLUGIN_JSON, JSON.parse(this.#text(PLUGIN_JSON)));
    }

    #text(path) {
        return readFileSync(join(this.#root, path), "utf8");
    }
}

// One kind of name the plugin has, such as its skills. fileOf(name) is
// the file that name comes from, or would come from; its frontmatter
// can declare the name again on a name: line.
export class PluginNames {
    #declared;

    constructor(kind, declared, fileOf) {
        this.kind = kind;
        this.#declared = declared;
        this.fileOf = fileOf;
    }

    get names() {
        return [...this.#declared.keys()];
    }

    has(name) {
        return this.#declared.has(name);
    }

    // The name on the file's name: line, or undefined when it has none.
    declaredName(name) {
        return this.#declared.get(name);
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

function declaredName(text) {
    const frontmatter = FRONTMATTER.exec(text)?.[1] ?? "";
    return NAME_LINE.exec(frontmatter)?.[1];
}
