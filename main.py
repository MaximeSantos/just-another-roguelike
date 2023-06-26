import tcod

from actions import EscapeAction, MovementAction
from input_handlers import EventHandler


def main() -> None:
    # variables
    screen_width = 80
    screen_height = 50
    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    event_handler = EventHandler()

    # screen creation
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Just Another Roguelike",
        vsync=True,
    ) as context:
        # console creation
        root_console = tcod.console.Console(screen_width, screen_height, order="F")

        # game loop
        while True:
            # adds our character to the console
            root_console.print(x=player_x, y=player_y, string="@")

            # screen update
            context.present(root_console)
            root_console.clear()

            # listens for event
            for event in tcod.event.wait():
                action = event_handler.dispatch(event)

                if action is None:
                    continue

                # checks is action is an instance of MovemementAction class
                if isinstance(action, MovementAction):
                    player_x += action.dx
                    player_y += action.dy

                elif isinstance(action, EscapeAction):
                    raise SystemExit()


if __name__ == "__main__":
    main()
