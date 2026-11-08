// The plugin as it is in this repo: the names a user sees.

import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const AGENT_SUFFIX = ".md";

export class Plugin {
    #root;

    constructor(root) {
        this.#root = root;
    }

    // One name per folder under skills/.
    get skills() {
        const folders = this.#entries("skills").filter((e) => e.isDirectory());
        return folders.map((folder) => folder.name);
    }

    // One name per file agents/<name>.md.
    get agents() {
        const files = this.#entries("agents").filter((e) => e.isFile());
        const agents = files.filter((e) => e.name.endsWith(AGENT_SUFFIX));
        return agents.map((e) => e.name.slice(0, -AGENT_SUFFIX.length));
    }

    // .claude-plugin/plugin.json, parsed.
    get manifest() {
        const path = join(this.#root, ".claude-plugin", "plugin.json");
        return JSON.parse(readFileSync(path, "utf8"));
    }

    #entries(folder) {
        return readdirSync(join(this.#root, folder), { withFileTypes: true });
    }
}
