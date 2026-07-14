from typing import Any, Callable
from desklab import Window, FlexBox, Text, Font, Color, Button
from src.interface._utils import toggle_brightness_up


def main_menu_setup(classify_menu: Window) -> Window:

    BASE_COLOR = Color((51, 36, 43))

    WINDOW_WIDTH = Window.get_width()
    WINDOW_HEIGHT = Window.get_height()

    HEADER_HEIGHT = 100
    BODY_HEIGHT = WINDOW_HEIGHT - HEADER_HEIGHT

    BUTTONS_CONTAINER_WIDTH = int(WINDOW_WIDTH / 2)
    BUTTONS_CONTAINER_HEIGHT = int(BODY_HEIGHT / 1.3)

    main_menu = Window()
    base = main_menu.add_layer()

    base.add_children(
        [
            header := FlexBox(WINDOW_WIDTH, HEADER_HEIGHT, color=BASE_COLOR),
            body := FlexBox(WINDOW_WIDTH, BODY_HEIGHT, color=BASE_COLOR.lightened(20))
        ]
    )

    default_font = Font("consolas", 40)

    header.add_children(
        Text("KNN CHARACTER RECOGNITION", default_font, "WHITE")
    )

    body.add_children(
        buttons_container := FlexBox(BUTTONS_CONTAINER_WIDTH, BUTTONS_CONTAINER_HEIGHT,
                                     space_between=24, corners_radius=40, color=BASE_COLOR)
    )

    buttons_text_corners_color_acion: list[tuple[str, tuple[int, int, int, int], tuple[int, ...], Callable[..., Any]]] = [
        ("START", (20, 20, 0, 0), (255, 147, 23), classify_menu.open),
        ("METRICS", (0, 0, 0, 0), (252, 70, 48), lambda: ...),
        ("EXIT", (0, 0, 20, 20), (227, 8, 66), main_menu.close)
    ]

    buttons_list: list[Button] = []

    for text, corners, color, action in buttons_text_corners_color_acion:

        width = int(BUTTONS_CONTAINER_WIDTH / 1.5)
        height = int(BUTTONS_CONTAINER_HEIGHT / 4.7)

        buttons_container.add_children(
            button := Button(width, height, corners_radius=corners, color=color, trigger_actions_on_release=True)
        )

        text_color = button.get_color().lightened(70)
        button.add_children(Text(text, default_font, text_color))
        toggle_brightness_up(button, 30)

        button.add_actions(action)
        buttons_list.append(button)

    return main_menu
