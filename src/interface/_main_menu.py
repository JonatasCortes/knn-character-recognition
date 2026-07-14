from dataclasses import dataclass
from typing import Any, Callable, Final
from desklab import Color, FlexBox, Window
from src.interface._utils import create_button_with_text, build_header


def main_menu_setup(classify_menu: Window) -> Window:

    BASE_COLOR: Final[Color] = Color((51, 36, 43))

    WINDOW_WIDTH: Final[int] = Window.get_width()
    WINDOW_HEIGHT: Final[int] = Window.get_height()

    HEADER_HEIGHT: Final[int] = 100
    BODY_HEIGHT: Final[int] = WINDOW_HEIGHT - HEADER_HEIGHT

    BUTTONS_CONTAINER_WIDTH: Final[int] = int(WINDOW_WIDTH / 2)
    BUTTONS_CONTAINER_HEIGHT: Final[int] = int(BODY_HEIGHT / 1.3)

    main_menu: Final[Window] = Window()

    @dataclass(frozen=True, slots=True)
    class ActionButtonSpec:
        text: str
        corners_radius: tuple[int, int, int, int]
        color: tuple[int, int, int]
        action: Callable[[], Any]

    def _build_buttons_container(width: int, height: int, on_metrics: Callable[[], Any]) -> FlexBox:
        container = FlexBox(width, height, space_between=24,
                            corners_radius=40, color=BASE_COLOR,)

        button_width = int(width / 1.5)
        button_height = int(height / 4.7)

        specs: tuple[ActionButtonSpec, ...] = (
            ActionButtonSpec("START", (20, 20, 0, 0),
                             (255, 147, 23), classify_menu.open),
            ActionButtonSpec("METRICS", (0, 0, 0, 0),
                             (252, 70, 48), on_metrics),
            ActionButtonSpec("EXIT", (0, 0, 20, 20),
                             (227, 8, 66), main_menu.close),
        )

        for spec in specs:
            container.add_children(
                create_button_with_text(
                    button_width,
                    button_height,
                    spec.color,
                    spec.text,
                    corners_radius=spec.corners_radius,
                    font_size=40,
                    action=spec.action,
                )
            )

        return container

    def _setup() -> Window:
        base_layer = main_menu.add_layer()

        header = build_header(WINDOW_WIDTH)
        body = FlexBox(WINDOW_WIDTH, BODY_HEIGHT,
                       color=BASE_COLOR.lightened(20))

        buttons_container = _build_buttons_container(
            BUTTONS_CONTAINER_WIDTH,
            BUTTONS_CONTAINER_HEIGHT,
            lambda: None,
        )
        body.add_children(buttons_container)

        base_layer.add_children([header, body])
        return main_menu

    return _setup()
