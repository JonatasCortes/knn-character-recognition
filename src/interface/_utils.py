from typing import Any, Callable

from desklab import FlexBox, Color, HoverListener, Button, Image


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
