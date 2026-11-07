# ntm

Your own settings and style for the ntm plugin (Neurodivergent Task Manager).
ntm itself holds nothing of yours; everything that is yours lives here, in two
skills:

- `ntm:settings`: what you agreed to during setup. Where your todo list is,
  your label names, how planning works for you, how the price watch judges a
  deal, how reminders reach you, and anything you do differently from ntm's
  conventions.
- `ntm:style`: how your reminders talk to you, and the skill that writes
  them that way. Either a profile you built with
  `/neurodivergent-task-manager:configure-style`, or a
  persona skill you already had, pasted in.

`/neurodivergent-task-manager:configure` builds this plugin with you and hands
it back to install.
`/neurodivergent-task-manager:settings` changes the settings;
`/neurodivergent-task-manager:configure-style` changes the style.
Each change hands you a new copy to install in place of this one.

Keep this plugin private. It can hold your Pushover keys. Share ntm, not this.

Nothing here sends data anywhere on its own; ntm's skills read it.
