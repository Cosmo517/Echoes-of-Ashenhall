from world.enemies.enemy_base import EnemyBase
import random

class Goblin(EnemyBase):
    def __init__(self, name='Goblin', hp=10, armor_class=8):
        super().__init__(name, hp, armor_class)
        self.display_char = 'g'
        self.weapons.append('Wooden Sword')

    def basic_attack(self):
        return random.randint(1, 4)

    def decide_action(self):
        # Possible actions the enemy can take
        actions = ["move, attack, flee, roam"]
        
        # For now, lets just make the enemy move randomly
        move_dict = {(0, -1), (-1, 0), (0, 1), (1, 0)}
        
        return move_dict[random.randint(0, 3)]