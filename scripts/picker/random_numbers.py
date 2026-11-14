class ParkMiller:
    MODULUS = 2_147_483_647
    MULTIPLIER = 48_271

    def __init__(self, state):
        self.state = state

    def __iter__(self):
        return self

    def __next__(self):
        self.state = self.state * self.MULTIPLIER % self.MODULUS
        return self.state


class RandomNumbers:
    # Park-Miller's first numbers follow a small seed closely.
    SKIPPED = 2

    def __init__(self, seed):
        self.states = ParkMiller(seed % (ParkMiller.MODULUS - 1) + 1)
        for _ in range(self.SKIPPED):
            next(self.states)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.states) / ParkMiller.MODULUS
