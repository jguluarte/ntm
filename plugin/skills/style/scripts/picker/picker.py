import contextlib
import sys


class Picker:
    def __init__(self, theme):
        self.theme = theme

    def pick(self):
        perspective = self.theme.draw_perspective()
        reference = self.theme.draw_reference_outside(perspective.kind)
        return perspective, reference


def pick_text(perspective, reference):
    return f"perspective: {perspective.name}\nreference: {reference.name}"


@contextlib.contextmanager
def reporting_failures():
    try:
        yield
    except Exception as failure:
        why = " ".join(str(failure).split())
        sys.exit(f"Picker FAILED: { type(failure).__name__ }: {why}")
