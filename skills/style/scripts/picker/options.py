import yaml

POOLS = "pools"
GIVES = "gives"
ENTRIES = "entries"
HOOK = "hook"


class Options:
    def __init__(self, fields):
        pools_by_kind = fields[POOLS]
        self.pools = [Pool(kind, pools_by_kind[kind]) for kind in pools_by_kind]

    @classmethod
    def load(cls, path):
        with open(path, encoding="utf-8") as file:
            return cls(yaml.safe_load(file))

    def hooks(self):
        hooks = []
        for pool in self.hook_pools():
            hooks.extend(pool.entries)
        return hooks

    def hook_pools(self):
        return [pool for pool in self.pools if pool.gives_hook()]


class Pool:
    def __init__(self, kind, fields):
        self.kind = kind
        self.gives = fields[GIVES]
        self.entries = [Entry(kind, slug) for slug in fields[ENTRIES]]

    def gives_hook(self):
        return HOOK in self.gives


class Entry:
    def __init__(self, kind, slug):
        self.kind = kind
        self.slug = slug

    def __str__(self):
        return f"{self.kind}/{self.slug}"
