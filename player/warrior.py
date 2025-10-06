from player.player import Player
import random

class Warrior(Player):
    def __init__(self, name='Adventurer', hp=15, armor_class=10):
        super().__init__(name, hp, 10, armor_class)
        self.weapons = ['Short Sword']
        self.armor = ['Chain Mail']
        
    def attack(self):
        to_hit = random.randint(1, 20)
        attack_daamge = random.randint(0, 6)
        return to_hit, attack_daamge