import random


class MyRandom:
    def __init__(self,trap_percentage):
        self.random = random
        self.trap_percentage = trap_percentage

    def choice(self, array):
        return self.random.choice(array)

    def is_normal(self):
        return self.trap_percentage < self.random.randint(1, 100)
