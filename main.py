from engine.player.warrior import Warrior
from engine.game_context import GameContext
from engine.game_manager import GameManager
from engine.systems.combat_system import CombatSystem
from engine.systems.dungeon_manager import DungeonManager
from engine.systems.input_system import InputSystem
from engine.systems.logging_system import LoggingSystem
from engine.systems.render_system import RenderSystem
from engine.systems.story_manager import StoryManager
from engine.event_bus import EventBus
from pathlib import Path
from engine.mods.mod_loader import ModLoader
import sys

base_path = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent

mods_path = base_path / "mods"

mod_loader = ModLoader(mods_path)
mods = mod_loader.load_all()

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
story_manager = StoryManager(game_context, mods)
game_manager = GameManager(game_context)

game_context.player = player_character
game_context.combatManager = combat_manager
game_context.dungeonManager = dungeon_manager
game_context.inputSystem = input_system
game_context.renderSystem = render_system
game_context.storyManager = story_manager
game_context.gameManager = game_manager


game_context.gameManager.start_game()