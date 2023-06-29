from typing import Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


class Engine:
    def __init__(
        self,
        event_handler: EventHandler,
        game_map: GameMap,
        player: Entity,
    ):
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()  # the function is actually called when Engine is instantiated, before the player has even moved

    def handle_event(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

            self.update_fov()  # updates the FOV before the player's next action

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
        context.present(console)
        console.clear()
