from typing import Any, Callable, Final
from desklab import FlexBox, Color, Font, HoverListener, Button, Image, Text

DEFAULT_FONT: Final[Font] = Font("consolas", 40)
HEADER_HEIGHT: Final[int] = 100
BASE_COLOR: Final[Color] = Color((51, 36, 43))


def build_header(width: int) -> FlexBox:
    header = FlexBox(width, HEADER_HEIGHT, color=BASE_COLOR)
    header.add_children(Text("KNN CHARACTER RECOGNITION",
                             DEFAULT_FONT, "WHITE"))
    return header


def toggle_color(flexbox: FlexBox, color: Color | str | tuple[int, ...]) -> None:
    default_color = flexbox.get_color()

    def _toggle():
        if flexbox.get_color() == default_color:
            flexbox.set_color(color)
        else:
            flexbox.set_color(default_color)
    flexbox.add_children(HoverListener(flexbox, _toggle, on_change=True))


def toggle_brightness_up(flexbox: FlexBox, intensity: int) -> None:
    toggle_color(flexbox, flexbox.get_color().lightened(intensity))


def toggle_luminance_emphasis(flexbox: FlexBox, intensity: int) -> None:
    toggle_color(flexbox, flexbox.get_color().luminance_emphasized(intensity))


def create_button_with_image(image_path: str, width: int, height: int, color: Color | str | tuple[int, ...], action: Callable[..., Any]) -> Button:
    btn = Button(width, height, color=color, bounded=False,
                 trigger_actions_on_release=True)

    img = Image(image_path).resized(width, height)
    img_scaled = img.rescaled(1.2)

    def toggle_scale():
        if btn.pop_child() is img:
            btn.add_children(img_scaled)
        else:
            btn.add_children(img)

    btn.add_children(
        [
            HoverListener(btn, toggle_scale, on_change=True),
            img
        ]
    )
    btn.add_actions(action)
    return btn


def create_button_with_text(width: int, height: int, color: Color | str | tuple[int, ...], text: str, *, corners_radius: int | tuple[int, int, int, int] = 20, font_size: int = 30, action: Callable[[], Any] | None = None,) -> Button:
    if action is None:
        def _action(): return None
        action = _action

    button = Button(width, height, action,
                    corners_radius=corners_radius,
                    color=color)

    toggle_brightness_up(button, 30)
    button.add_children(Text(text, DEFAULT_FONT.copy(size=font_size),
                             button.get_color().lightened(90)))
    return button
