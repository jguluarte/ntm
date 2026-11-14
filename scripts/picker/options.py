from failure import PickerFailed

POOLS = "pools"
GIVES = "gives"
ENTRIES = "entries"
HOOK = "hook"


class Options:
    def __init__(self, fields):
        listed = fields.get(POOLS) if isinstance(fields, dict) else None
        if not isinstance(listed, dict):
            raise PickerFailed("the options file has no pools")
        pools = [Pool(kind, pool) for kind, pool in listed.items()]
        self.entries = [entry for pool in pools for entry in pool.entries]

    def hooks(self):
        return [entry for entry in self.entries if entry.pool.gives(HOOK)]


class Pool:
    def __init__(self, kind, fields):
        if not self._well_formed(fields):
            raise PickerFailed(f"pool {kind} needs gives and entries")
        self.kind = kind
        self.given = fields[GIVES]
        self.entries = [Entry(self, slug) for slug in fields[ENTRIES]]

    def gives(self, role):
        return role in self.given

    @staticmethod
    def _well_formed(fields):
        shape = fields if isinstance(fields, dict) else {}
        has_gives = isinstance(shape.get(GIVES), list)
        has_entries = isinstance(shape.get(ENTRIES), dict)
        return has_gives and has_entries


class Entry:
    def __init__(self, pool, slug):
        self.pool = pool
        self.id = f"{pool.kind}/{slug}"
