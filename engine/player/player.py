class Player:
    def __init__(self, name, gold, hp, armor_class):
        self.name = name
        self.armor_class = armor_class
        self.hp = hp
        self.gold = gold
        self.items = []  # anything that isnt a weapon/armor
        self.weapons = []
        self.armor = []
        
    def set_hp(self, hp):
        self.hp = hp
    
    def hit(self, damage):
        self.hp = self.hp - damage
    
    def get_hp(self):
        return self.hp

    def set_armor_class(self, ac):
        self.armor_class = ac