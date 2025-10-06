from player.warrior import Warrior
from world.dungeons.Dungeon import Dungeon
import keyboard

player_character = Warrior("test")

test_maze = Dungeon(20, 20)
test_maze.enter_dungeon(player_character)
test_maze.print_dungeon()

moves = ['w', 'a', 's', 'd']

# Simple game loop for capturing player input
while True:
    event = keyboard.read_event()
    if event.event_type == keyboard.KEY_DOWN:
        if event.name in moves:
            test_maze.handle_player_movement(event.name)