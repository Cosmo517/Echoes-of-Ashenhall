from player.warrior import Warrior
from game_context import GameContext
from game_manager import GameManager
from systems.combat_system import CombatSystem
from systems.dungeon_manager import DungeonManager
from systems.input_system import InputSystem
from systems.logging_system import LoggingSystem
from systems.render_system import RenderSystem
from systems.story_manager import StoryManager
from event_bus import EventBus

game_context = GameContext()

player_character = Warrior("test")

event_bus = EventBus(game_context)
game_context.event_bus = event_bus

logging_system = LoggingSystem(game_context)
game_context.loggingSystem = logging_system

combat_manager = CombatSystem(game_context)
dungeon_manager = DungeonManager(game_context)
input_system = InputSystem(game_context)
render_system = RenderSystem(game_context)
story_manager = StoryManager(game_context)
game_manager = GameManager(game_context)

game_context.player = player_character
game_context.combatManager = combat_manager
game_context.dungeonManager = dungeon_manager
game_context.inputSystem = input_system
game_context.renderSystem = render_system
game_context.storyManager = story_manager
game_context.gameManager = game_manager


game_context.gameManager.start_game()