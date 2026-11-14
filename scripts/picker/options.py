from failure import PickerFailed

HOOK = "hook"


class Options:
    def __init__(self, fields):
        pools = fields.get("pools") if isinstance(fields, dict) else None
        if not isinstance(pools, dict):
            raise PickerFailed("the options file has no pools")
        self.pools = [Pool(kind, pool) for kind, pool in pools.items()]
        self.entries = [entry for pool in self.pools for entry in pool.entries]

    def hooks(self):
        return [entry for entry in self.entries if entry.pool.gives(HOOK)]


class Pool:
    def __init__(self, kind, fields):
        if not self._well_formed(fields):
            raise PickerFailed(f"pool {kind} needs gives and entries")
        self.kind = kind
        self.roles = fields["gives"]
        entries = fields["entries"]
        self.entries = [Entry(self, slug) for slug in entries]

    def gives(self, role):
        return role in self.roles

    @staticmethod
    def _well_formed(fields):
        shape = fields if isinstance(fields, dict) else {}
        has_gives = isinstance(shape.get("gives"), list)
        has_entries = isinstance(shape.get("entries"), dict)
        return has_gives and has_entries


class Entry:
    def __init__(self, pool, slug):
        self.pool = pool
        self.id = f"{pool.kind}/{slug}"
