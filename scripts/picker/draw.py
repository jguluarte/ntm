class Draw:
    def __init__(self, items):
        self.items = list(items)

    def pick(self, random_number):
        return self.items[int(random_number * len(self.items))]
