// User-facing names change only with Justin's explicit yes.
//
// These tests compare the names the plugin has with the names Justin
// expects, which live in tests/expected/. A rename fails here until he
// updates that folder himself. See tests/expected/README.md.

import { join } from "node:path";
import { describe, test } from "node:test";
import { NamesCheck, PluginJsonCheck } from "./support/checks.mjs";
import { Expectations } from "./support/expectations.mjs";
import { Plugin } from "./support/plugin.mjs";

const REPO = join(import.meta.dirname, "..");

// Every file is read here, before the tests are defined: a file that
// can't be read fails the whole run, rather than one test quietly.
const plugin = new Plugin(REPO);
const expected = new Expectations(REPO);

const skills = new NamesCheck(plugin.skills, expected.skills);
const agents = new NamesCheck(plugin.agents, expected.agents);
const pluginJson = new PluginJsonCheck(plugin.pluginJson, expected.pluginJson);

describe("skills: one folder under skills/ per skill", () => {
    test("no skill exists that Justin didn't expect", () => {
        skills.assertNoneUnexpected();
    });

    test("every skill Justin expects exists", () => {
        skills.assertNoneMissing();
    });
});

describe("agents: one file agents/<name>.md per agent", () => {
    test("no agent exists that Justin didn't expect", () => {
        agents.assertNoneUnexpected();
    });

    test("every agent Justin expects exists", () => {
        agents.assertNoneMissing();
    });
});

describe("plugin.json: the values Justin expects", () => {
    for (const [field, value] of expected.pluginJson.fields) {
        test(`${field} is ${JSON.stringify(value)}`, () => {
            pluginJson.assertField(field);
        });
    }
});
