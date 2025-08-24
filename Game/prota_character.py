import random

class Prota:
    def __init__(self, hp, damage, lives, parry_prob):
        self.hp = hp
        self.damage = damage
        self.lives = lives
        self.parry_prob = parry_prob
        self.name = "default"

    def hurt(self, other):
        damage = self.damage

        if random.random() <= self.parry_prob:
            #acá se define el area de danio

    def set_name(self, name):
        self.name = name
