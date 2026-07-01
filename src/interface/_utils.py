from desklab import FlexBox, Color, HoverListener


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
