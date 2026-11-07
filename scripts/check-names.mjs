// The names check: the plugin's name and displayName, the skill folders and
// the agent files must match names.txt, the list of user-facing names that
// only Justin edits. Any difference fails with the names added and removed,
// so no rename lands without his change to names.txt.

import { existsSync, readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const NAMES_FILE = "names.txt";
const PLUGIN_FILE = ".claude-plugin/plugin.json";
const SKILLS_DIR = "skills";
const SKILL_FILE = "SKILL.md";
const AGENTS_DIR = "agents";
const AGENT_SUFFIX = ".md";
const COMMENT = "#";

const MISMATCH = [
    "User-facing names changed. names.txt must change too, and only Justin",
    "edits names.txt. Ask him.",
].join("\n");

class RepoNames {
    static all() {
        const names = [
            ...RepoNames.#plugin(),
            ...RepoNames.#skills(),
            ...RepoNames.#agents(),
        ];

        return new Set(names);
    }

    static #plugin() {
        const plugin = JSON.parse(readFileSync(PLUGIN_FILE, "utf8"));

        return [plugin.name, plugin.displayName];
    }

    // A skill is a folder holding SKILL.md, as the plugin loader sees it; a
    // folder git left behind with only untracked files in it isn't one.
    static #skills() {
        const entries = readdirSync(SKILLS_DIR, { withFileTypes: true });
        const isSkill = (entry) =>
            entry.isDirectory() &&
            existsSync(join(SKILLS_DIR, entry.name, SKILL_FILE));

        return entries.filter(isSkill).map((entry) => entry.name);
    }

    static #agents() {
        const files = readdirSync(AGENTS_DIR);
        const agents = files.filter((file) => file.endsWith(AGENT_SUFFIX));

        return agents.map((file) => file.slice(0, -AGENT_SUFFIX.length));
    }
}

class NamesList {
    static read() {
        const lines = readFileSync(NAMES_FILE, "utf8").split(/\r?\n/);
        const names = lines.map((line) => line.trim());
        const isName = (name) => name !== "" && !name.startsWith(COMMENT);

        return new Set(names.filter(isName));
    }
}

const inRepo = RepoNames.all();
const listed = NamesList.read();
const added = [...inRepo].filter((name) => !listed.has(name)).sort();
const removed = [...listed].filter((name) => !inRepo.has(name)).sort();

if (added.length > 0 || removed.length > 0) {
    console.error(MISMATCH);

    if (added.length > 0) {
        console.error("\nAdded (in the repo, not in names.txt):");
        for (const name of added) console.error(`    ${name}`);
    }

    if (removed.length > 0) {
        console.error("\nRemoved (in names.txt, not in the repo):");
        for (const name of removed) console.error(`    ${name}`);
    }

    process.exit(1);
}
