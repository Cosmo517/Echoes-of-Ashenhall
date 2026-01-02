class Tile:
    def __init__(self, display_char=' ', walkable=True, item=None, entity=None):
        self.display_char = display_char
        self.item = item
        self.entity = entity
        
        # Can the player/enemy walk on this tile
        self.walkable = walkable
        
    def is_walkable(self):
        return self.walkable
    
    def set_walkable(self, walkable):
        self.walkable = walkable
    
    def set_wall(self):
        self.walkable = False
        self.display_char = "#"

    def has_entity(self):
        """Returns true if an entity is on the tile"""
        return True if self.entity else False
    
    def get_display_char(self):
        """Returns the display character of the tile"""
        return self.display_char

    def get_item(self):
        """Returns the item on the tile"""
        return self.item

    def get_entity(self):
        """Returns the entity on the tile"""
        return self.entity if self.entity else None

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
