from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING

import numpy as np
from tcod.console import Console

from entity import Actor
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class GameMap:
    def __init__(
        self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()
    ):
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)
        # create 2D arrays, filled with the same values, walls by default, or False for our visible & explored tiles
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
        self.visible = np.full(
            (width, height), fill_value=False, order="F"
        )  # tiles the player can currently see
        self.explored = np.full(
            (width, height), fill_value=False, order="F"
        )  # tiles the player has seen

    @property
    def actors(self) -> Iterable[Actor]:
        """Iterate over this maps living actors"""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

    def get_blocking_entity_at_location(
        self, location_x: int, location_y: int
    ) -> Optional[Entity]:
        """
        Iterates through all the entities, and if one is found to both blocks movement and
        occupies the given location_x and location_y coordinates,
        it returns that Entity. Otherwise, we return None
        """
        for entity in self.entities:
            if (
                entity.blocks_movement
                and entity.x == location_x
                and entity.y == location_y
            ):
                return entity
        return None

    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor
        return None

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
        Renders the map.

        If a tile is in the "visible" array, then draw it with the "light" colors.
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
        Otherwise, the default is "SHROUD".
        """
        # console.rgb much faster than console.print to render entire map
        console.rgb[0 : self.width, 0 : self.height] = np.select(
            # condlist sets the conditions, first checks if tile is visible, then if it is explored
            condlist=[self.visible, self.explored],
            # choicelist selects the proper value depending on if it passed the first or second condition
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            # if it passed neither, then it gets the default value in SHROUD
            default=tile_types.SHROUD,
        )

        """
        The sorted function takes two arguments: The collection to sort, and the function used to sort it. By using key in sorted, here we're using a lambda function
        (basically, a function that's limited to one line that we don't need to write a formal definition for)
        The lambda function itself tells sorted to sort by the value of render_order.
        Since the RenderOrder enum defines its order from 1 (Corpse, lowest) to 3 (Actor, highest),
        corpses should be sent to the front of the sorted list and drawn first. Then overriden by "higher ranked" entities.
        """
        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda x: x.render_order.value
        )

        for entity in entities_sorted_for_rendering:
            # only prints entity within the FOV
            if self.visible[entity.x, entity.y]:
                console.print(
                    x=entity.x, y=entity.y, string=entity.char, fg=entity.color
                )
