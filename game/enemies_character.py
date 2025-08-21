import random

class Enemies:
    def __init__(self, hp, damage, counter, collapse_prob):
        self.hp = hp
        self.damage = damage
        self.counter = counter
        self.collapse_prob = collapse_prob
        self.name = "default"

    def attack(self, other):
        damage = self.damage

        if random.random() <= self.collapse_prob:
            #prota recibe daño

    def set_name(self, name):
        self.name = name
