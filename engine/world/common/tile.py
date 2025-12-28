class Tile:
    def __init__(self, display_char=' ', item=None, entity=None):
        self.display_char = display_char
        self.item = item
        self.entity = entity
        # Can the player/enemy walk on this tile
        self.player_walkable = True
        self.enemy_walkable = True

    def can_player_walk(self):
        """Checks to see if a player can walk on this tile"""
        return self.player_walkable
    
    def can_enemy_walk(self):
        """Checks to see if an enemy can walk on this tile"""
        return self.enemy_walkable

    def has_entity(self):
        """Returns true if an entity is on the tile"""
        if self.entity:
            return True
        else:
            return False
    
    def get_display_char(self):
        """Returns the display character of the tile"""
        return self.display_char

    def get_item(self):
        """Returns the item on the tile"""
        return self.item

    def get_entity(self):
        """Returns the entity on the tile"""
        return self.entity if self.entity else None
    
    def get_player_walkable(self):
        return self.player_walkable
    
    def get_enemy_walkable(self):
        return self.enemy_walkable

    def set_display_char(self, new_char):
        """Sets the display character of a tile"""
        self.display_char = new_char

    def set_item(self, new_item):
        """Sets the item on the tile"""
        self.item = new_item

    def set_entity(self, new_entity):
        """Sets the entity on the tile"""
        self.entity = new_entity
        if self.entity is not None:
            self.walkable = False
        else:
            self.walkable = True
            
    def set_player_walkable(self, walk):
        self.player_walkable = walk
    
    def set_enemy_walkable(self, walk):
        self.enemy_walkable = walk
    
    def set_walkable(self, walk):
        self.player_walkable = walk
        self.enemy_walkable = walk