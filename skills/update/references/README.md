# Update notes

One note per version of ntm, named for the version, such as `0.5.0.md`.
`ntm:update` reads each note newer than the user's version, oldest first. A note
has two parts:

| Part           | What it holds                                               |
| -------------- | ----------------------------------------------------------- |
| What's new     | The changelog, for the user, in plain words                 |
| For ntm:update | What to offer or do for a user coming from an older version |

For ntm:update ends with `Rebuild ntm-user: yes` or `Rebuild ntm-user: no`.
