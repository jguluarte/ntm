// User-facing names change only with Justin's explicit yes.
//
// These tests compare the names the plugin has with the names Justin
// expects, which live in tests/expected/. A rename fails here until he
// updates that folder himself; a local hook blocks every Claude session
// from editing it. See tests/expected/README.md.

import { join } from "node:path";
import { describe, test } from "node:test";
import { Expectations } from "./support/expectations.mjs";
import { Plugin } from "./support/plugin.mjs";

const REPO = join(import.meta.dirname, "..");

const plugin = new Plugin(REPO);
const expected = new Expectations(REPO);

describe("skills: one folder under skills/ per skill", () => {
    test("no skill exists that Justin didn't expect", () => {
        expected.skills.assertNoneUnexpected(plugin.skills);
    });

    test("every skill Justin expects exists", () => {
        expected.skills.assertNoneMissing(plugin.skills);
    });
});

describe("agents: one file agents/<name>.md per agent", () => {
    test("no agent exists that Justin didn't expect", () => {
        expected.agents.assertNoneUnexpected(plugin.agents);
    });

    test("every agent Justin expects exists", () => {
        expected.agents.assertNoneMissing(plugin.agents);
    });
});

describe("plugin.json: the fields Justin fixes", () => {
    for (const [field, value] of expected.manifest.fields) {
        test(`${field} is ${JSON.stringify(value)}`, () => {
            expected.manifest.assertField(field, plugin.manifest);
        });
    }
});
