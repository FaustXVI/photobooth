import random


class MyRandom:
    def __init__(self,percentage):
        self.random = random
        self.percentage = percentage

    def choice(self, array):
        return self.random.choice(array)

    def is_normal(self):
        return self.random.randint(1, 100) <= self.percentage
