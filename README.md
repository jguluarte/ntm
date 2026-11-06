# nudge

A personal task-nudging system that runs on your own ticket board and a few scheduled tasks. It plans one task per weekday, reminds you about it in a voice you pick, tells you in the evening how the day went, recaps and plans every week, and can watch prices on things you want to buy.

It was built by one person for the places that got in their way: starting tasks, keeping multi-day work moving, and noticing when things have quietly gone stale. It stays deliberately low-process. If it starts bogging you down, turn pieces off.

## How it works

- **Your board** is the source of truth. A ticket's planned date is the day you'll do it. Planners set those dates; you can set them yourself too, and a day you dated counts as planned.
- **Jobs** (scheduled tasks) run the skills on a schedule: a morning plan, an afternoon nudge, an evening check-in, a weekly recap and plan, and an optional daily price watch. Each job's procedure is a skill of its own, so you can also run one by hand ("run the morning plan now").
- **The messenger** writes every reminder from a profile you design with `nudge:messenger`: who is talking, what gets you to read, what happens when something keeps slipping. The profile lives in a note on your board, and the voice keeps a history so lines stay fresh.
- **Days off** stop automatic planning. Work you dated yourself for a day off still gets its reminders.
- **Grooming** happens in chat when you ask: closing obsolete tickets, sizing and splitting the rest.

## Getting started

1. Install the plugin and open a chat.
2. Make sure your tracker is connected. Linear is free for individuals and is the tested path; other trackers work through an adapter drafted during setup.
3. Run `/nudge:setup`. It asks about your tracker, notifications, price watch and rhythm, designs your messenger with `nudge:messenger`, hands you a personalized copy of the plugin and creates your scheduled tasks.
4. Install the personalized copy in place of this one. It holds your values (and, if you chose Pushover, your credentials), so keep it private.

## Components

- **Skills**: the knowledge and procedures, one each, listed below. Jobs and agents load them by name.
- **Agents**: the roles. The **planner** decides what you work on: it makes today ready in the morning, plans the week, and answers "what's due"; `/nudge:plan --weekly --replan` plans the week with you in chat. The **messenger** reaches you: given the facts of a run: morning, afternoon, evening or week, it writes the message the way your profile says you'll read it and sends it through your channel. The **price-checker** runs one purchase ticket's price check.
- **MCP servers**: Linear, the included tracker connector.

## Skills

| Skill | What it does |
| --- | --- |
| `nudge:setup` | One-time onboarding. Produces your personalized copy and your scheduled tasks. |
| `nudge:board` | The board's rules. Every other skill loads it first. |
| `nudge:ping` | Checks the session can reach your board. |
| `nudge:adapter` | Drafts an adapter for another tracker with you and smoke-tests it on your board. |
| `nudge:days-off` | Days off. |
| `nudge:due` | What's due. |
| `nudge:recap` | What got done over a span. |
| `nudge:plan` | Plans the week or today. |
| `nudge:cleanup` | Closes finished parents and clears stale dates. |
| `nudge:groom` | Grooms the board with you in chat. |
| `nudge:messenger` | Sets up or revises the messenger profile with you and saves it to its note. |
| `nudge:voice` | Rewrites a message the way your messenger profile says it gets read. |
| `nudge:notify` | Sends a notification through your chosen channel. |
| `nudge:morning` | The morning plan: carries missed work to today, plans today if it's empty, sends the morning message. |
| `nudge:afternoon` | The afternoon nudge: a friendly poke about what's still planned for today. |
| `nudge:evening` | The evening check-in: what closed, what's still open. |
| `nudge:week` | The weekly recap and plan: recap, cleanup, next week, one message. |
| `nudge:jobs` | Creates and maintains the scheduled tasks that run the four above and the price watch. |
| `nudge:price-watch` | Daily price check on purchase tickets. Optional. |
| `nudge:amazon-alerts` | Keeps Amazon's own price alerts in step with your watch list, from your computer. Optional. |

## Requirements

- A ticket tracker connected to Claude. Linear is supported out of the box; any tracker with a connector can be adapted with `nudge:adapter`, and `claude-docs` (a board kept in a Claude Doc) needs no tracker connector, only Claude Docs.
- Scheduled tasks available on your Claude account.
- For Pushover notifications: a Pushover account, an application token and your user key.
- For Amazon alert sync: Claude in Chrome on your computer.

## Privacy

The template plugin holds no personal values. Your personalized copy does. Share the template, not your copy.
