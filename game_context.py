class GameContext:
    def __init__(self):
        self.event_bus = None               # Global event system
        
        self.player = None                  # Player instance
        self.inventory = []                 # Players inventory
        
        self.flags = []                     # Gameplay flags
        
        self.current_scene = "intro"        # Json File
        self.current_level = "1"            # Folder
        self.state = "story"                # Game State (story/dungeon)
        
        self.combatManager = None           # CombatManager
        self.dungeonManager = None          # DungeonManager
        self.inputSystem = None             # InputSystem
        self.renderSystem = None            # RenderSystem
        self.storyManager = None            # StoryManager
        self.loggingSystem = None           # LoggingSystem
        self.gameManager = None             # GameManager