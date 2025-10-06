from world.enemies.basic_enemy import Enemy


class Goblin(Enemy):
    def __init__(self, name='Goblin', hp=10, armor_class=8):
        super().__init__(name, hp, armor_class)
        self.display_char = 'g'
        self.weapons.append('Wooden Sword')  # testing purposes for now

    def basic_attack(self):
        pass

    def movement(self):
        pass