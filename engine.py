from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from input_handlers import MainGameEventHandler

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap
    from input_handlers import EventHandler


class Engine:
    game_map: GameMap

    def __init__(self, player: Actor):
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.player = player

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        # compute_fov will return an array of visible tiles
        # https://python-tcod.readthedocs.io/en/latest/tcod/map.html#tcod.map.compute_fov for the complete documentation
        self.game_map.visible[:] = compute_fov(
            # transparency : takes a 2D numpy array, and considers any non-zero values to be transparent
            self.game_map.tiles["transparent"],
            # pov : origin point for the FOV
            (self.player.x, self.player.y),
            # radius : distance to which the FOV extends
            radius=8,
        )
        # if a tile is "visible" it should be added to "explored"
        # sets the explored array to include everything in the visible array, plus whatever it already had
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)
        console.print(
            x=1, y=47, string=f"{self.player.fighter.hp}/{self.player.fighter.max_hp}"
        )
        context.present(console)
        console.clear()
