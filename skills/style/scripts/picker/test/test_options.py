import unittest

from fixtures import EVEN, EVEN_HOOKS
from options import Options


class HooksTest(unittest.TestCase):
    def test_the_hooks_are_the_entries_of_pools_giving_a_hook(self):
        hooks = [str(hook) for hook in Options.load(EVEN).hooks()]
        self.assertEqual(EVEN_HOOKS, hooks)
