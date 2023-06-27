import numpy as np
from tcod.console import Console

import tile_types


class GameMap:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        # create 2D arrays, filled with the same values, walls by default, or False for our visible & explored tiles
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")

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
