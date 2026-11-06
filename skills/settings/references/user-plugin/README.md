# ntm-user

Your own settings and style for the ntm plugin (Neurodivergent Task Manager). ntm itself holds nothing of yours; everything that is yours lives here, in two skills:

- `ntm-user:settings`: what you agreed to during setup. Where your todo list is, your label names, how planning works for you, how the price watch judges a deal, how reminders reach you, and anything you do differently from ntm's conventions.
- `ntm-user:style`: how your reminders talk to you, and the skill that writes them that way. Either a profile you built with `/ntm:configure-style`, or a persona skill you already had, pasted in.

`/ntm:configure` builds this plugin with you and hands it back to install. `/ntm:settings` changes the settings; `/ntm:configure-style` changes the style. Each change hands you a new copy to install in place of this one.

Keep this plugin private. It can hold your Pushover keys. Share ntm, not this.

Nothing here sends data anywhere on its own; ntm's skills read it.
