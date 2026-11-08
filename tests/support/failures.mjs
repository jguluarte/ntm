// How a name test fails, in words for a person. No stack trace: where
// the error was thrown tells the reader nothing, the message says it all.

const EXPECTED_FOLDER = "tests/expected/";

class PlainFailure extends Error {
    constructor(message) {
        super(message);
        this.name = this.constructor.name;
        this.stack = `${this.name}: ${message}`;
    }
}

// A user-facing name changed without Justin's yes. Lists each change,
// then what to do next and which expectation file covers it.
export class NameChangeNotApproved extends PlainFailure {
    constructor(changes, file) {
        super([...changes, "", ...nextSteps(file)].join("\n"));
    }
}

// A file in tests/expected/ can't be used: missing, not valid JSON, or
// empty. Only Justin edits that folder, so the fix is his.
export class BrokenExpectationFile extends PlainFailure {
    constructor(file, problem) {
        const owner = `Only Justin edits ${EXPECTED_FOLDER}; he fixes it.`;
        super(`${file} ${problem}\n\n${owner}`);
    }
}

function nextSteps(file) {
    return [
        "User-facing names change only with Justin's explicit yes.",
        "  Didn't mean to change a name? Put it back.",
        `  Meant to? Ask Justin on the PR, and leave ${EXPECTED_FOLDER} alone.`,
        `  With his yes, he updates ${file} himself.`,
    ];
}
