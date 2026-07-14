from dataclasses import dataclass
from functools import partial
from typing import Any, Callable, Final
from desklab import Button, Color, DrawingArea, FlexBox, Font, Text, Window
from src.interface._utils import create_button_with_image, toggle_brightness_up


def classify_menu_setup() -> Window:

    BASE_COLOR: Final[Color] = Color((51, 36, 43))
    CORRECT_COLOR: Final[tuple[int, int, int]] = (120, 208, 98)
    INCORRECT_COLOR: Final[tuple[int, int, int]] = (227, 8, 66)

    DEFAULT_FONT: Final[Font] = Font("consolas", 40)
    DISPLAY_FONT: Final[Font] = Font("trebuchet", 150)

    HEADER_HEIGHT: Final[int] = 100
    COLOR_PALETTE_HEIGHT: Final[int] = 70
    COLOR_PALETTE_SPACE_BETWEEN: Final[int] = 20

    ASSETS_PATH: Final[str] = "src/interface/_assets/"
    TOOL_ICONS: Final[tuple[str, ...]] = ("pencil.png", "filler.png",
                                          "eraser.png", "clearer.png")

    BRUSH_COLORS: Final[tuple[tuple[tuple[int, int, int], int], ...]] = (
        ((24, 18, 30), 15),
        ((244, 91, 105), 20),
        ((255, 183, 3), 40),
        ((33, 158, 188), 30),
        ((142, 202, 230), 40),
        ((29, 53, 87), 15),
        ((172, 96, 172), 20),
        ((138, 191, 126), 30),
        ((250, 240, 228), -300),
        ((224, 122, 95), 30),
    )

    MODAL_WIDTH: Final[int] = 500
    MODAL_HEIGHT: Final[int] = 500
    MODAL_HEADER_HEIGHT: Final[int] = 70
    MODAL_BODY_HEIGHT: Final[int] = MODAL_HEIGHT - MODAL_HEADER_HEIGHT
    MODAL_BODY_PADDING: Final[int] = 25
    MODAL_BODY_SPACE_BETWEEN: Final[int] = 25
    MODAL_CONTENT_WIDTH: Final[int] = MODAL_WIDTH - 2 * MODAL_BODY_PADDING

    VERDICT_CONTAINER_HEIGHT: Final[int] = 120
    VERDICT_BUTTON_HEIGHT: Final[int] = 80
    VERDICT_BUTTON_SPACE_BETWEEN: Final[int] = 20
    RESULT_DISPLAY_HEIGHT: Final[int] = (
        MODAL_BODY_HEIGHT - 2 * MODAL_BODY_PADDING -
        MODAL_BODY_SPACE_BETWEEN - VERDICT_CONTAINER_HEIGHT
    )

    @dataclass(frozen=True, slots=True)
    class ActionButtonSpec:
        text: str
        color: tuple[int, int, int]
        corners_radius: tuple[int, int, int, int]
        action: Callable[[], Any]

    def _create_styled_button(width: int, height: int, color: Color | str | tuple[int, ...], text: str, *, corners_radius: int | tuple[int, int, int, int] = 20, font_size: int = 30, action: Callable[[], Any] | None = None,) -> Button:
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

    def _create_display_box(width: int, height: int, color: Color | str | tuple[int, ...], text: str, font: Font, corners_radius: int | tuple[int, int, int, int] = 40,) -> FlexBox:
        display = FlexBox(width, height,
                          corners_radius=corners_radius,
                          color=color)
        display.add_children(Text(text, font, "WHITE"))
        return display

    def _build_header(width: int) -> FlexBox:
        header = FlexBox(width, HEADER_HEIGHT, color=BASE_COLOR)
        header.add_children(Text("KNN CHARACTER RECOGNITION",
                                 DEFAULT_FONT, "WHITE"))
        return header

    def _build_color_palette(width: int, drawing_area: DrawingArea, palette_color: Color) -> FlexBox:
        color_palette = FlexBox(width, COLOR_PALETTE_HEIGHT, 0,
                                COLOR_PALETTE_SPACE_BETWEEN, "ROW",
                                color=palette_color)

        for color, emphasis_intensity in BRUSH_COLORS:
            brush_button = Button(50, 50, corners_radius=20, color=color)
            toggle_brightness_up(brush_button, emphasis_intensity)
            brush_button.add_actions(
                partial(drawing_area.set_brush_color, color))
            color_palette.add_children(brush_button)

        tool_actions: tuple[Callable[..., Any], ...] = (drawing_area.draw, drawing_area.fill,
                                                        drawing_area.erase, drawing_area.clear)
        color_palette.add_children(
            [
                create_button_with_image(f"{ASSETS_PATH}{icon}", 50,
                                         50, palette_color, action)
                for icon, action in zip(TOOL_ICONS, tool_actions)
            ]
        )
        return color_palette

    def _build_info_menu(width: int, height: int, color: Color, on_classify: Callable[[], Any], on_return: Callable[[], Any],) -> tuple[FlexBox, FlexBox]:
        info_menu = FlexBox(width, height, (0, 0, 10, 0), 30,
                            color=color, vertical_alignment="BOTTOM")

        classification_display = _create_display_box(int(width / 1.2), int(height / 3),
                                                     color.lightened(20), "N/A", DISPLAY_FONT)
        buttons_container = FlexBox(int(width / 1.2), int(height / 2),
                                    space_between=20, corners_radius=40,
                                    color=BASE_COLOR.lightened(10))
        button_width = int(width / 1.44)
        button_height = int(height / 6)

        specs: tuple[ActionButtonSpec, ...] = (
            ActionButtonSpec("CLASSIFY", CORRECT_COLOR,
                             (20, 20, 0, 0), on_classify),
            ActionButtonSpec("RETURN", INCORRECT_COLOR,
                             (0, 0, 20, 20), on_return),
        )
        for spec in specs:
            buttons_container.add_children(
                _create_styled_button(
                    button_width, button_height, spec.color, spec.text,
                    corners_radius=spec.corners_radius, action=spec.action,
                )
            )

        info_menu.add_children([classification_display, buttons_container])
        return info_menu, classification_display

    def _build_classify_modal(modal_layer: FlexBox, close_modal: Callable[[], Any]) -> FlexBox:

        modal_background = FlexBox(MODAL_WIDTH, MODAL_HEIGHT, corners_radius=20,
                                   color=BASE_COLOR.lightened(70))

        modal_layer.add_children(modal_background)

        modal_header = FlexBox(MODAL_WIDTH, MODAL_HEADER_HEIGHT, 0, 70, "ROW", "LEFT",
                               corners_radius=(20, 20, 0, 0), color=BASE_COLOR.lightened(20))

        modal_body = FlexBox(MODAL_WIDTH, MODAL_BODY_HEIGHT, MODAL_BODY_PADDING, MODAL_BODY_SPACE_BETWEEN,
                             corners_radius=(0, 0, 20, 20), color=BASE_COLOR.lightened(70))

        modal_background.add_children([modal_header, modal_body])

        close_modal_button = _create_styled_button(70, MODAL_HEADER_HEIGHT, INCORRECT_COLOR, "X",
                                                   corners_radius=(10, 0, 0, 0), action=close_modal)

        modal_title = Text(
            "CLASSIFICATION", DEFAULT_FONT.copy(size=30), "WHITE")
        modal_header.add_children([close_modal_button, modal_title])

        result_display = _create_display_box(MODAL_CONTENT_WIDTH, RESULT_DISPLAY_HEIGHT, BASE_COLOR.lightened(40),
                                             "N/A", DISPLAY_FONT, corners_radius=30,)

        verdict_buttons = FlexBox(MODAL_CONTENT_WIDTH, VERDICT_CONTAINER_HEIGHT, 15,
                                  VERDICT_BUTTON_SPACE_BETWEEN, "ROW", corners_radius=30,
                                  color=BASE_COLOR.lightened(20))

        verdict_button_width = (MODAL_CONTENT_WIDTH -
                                2 * 15 - VERDICT_BUTTON_SPACE_BETWEEN) // 2

        verdict_buttons.add_children(
            [
                _create_styled_button(verdict_button_width, VERDICT_BUTTON_HEIGHT,
                                      CORRECT_COLOR, "CORRECT", corners_radius=(20, 0, 20, 0), font_size=30),
                _create_styled_button(verdict_button_width, VERDICT_BUTTON_HEIGHT,
                                      INCORRECT_COLOR, "INCORRECT", corners_radius=(0, 20, 0, 20), font_size=30),
            ]
        )

        modal_body.add_children([result_display, verdict_buttons])
        return result_display

    def _setup() -> Window:
        window_width = Window.get_width()
        window_height = Window.get_height()

        drawing_area_width = int(window_width / 1.5)
        info_menu_width = window_width - drawing_area_width
        body_height = window_height - HEADER_HEIGHT - COLOR_PALETTE_HEIGHT

        info_menu_color = BASE_COLOR.lightened(20)
        palette_color = BASE_COLOR.lightened(10)

        classify_menu = Window()
        base_layer = classify_menu.add_layer()
        modal_layer = classify_menu.add_layer(color=(0, 0, 0, 150),
                                              visible=False)

        def open_modal() -> None:
            modal_layer.set_visibility(True)

        def close_modal() -> None:
            modal_layer.set_visibility(False)

        drawing_area = DrawingArea(drawing_area_width, body_height, 0,
                                   BASE_COLOR.lightened(30), eraser_width=20)

        header = _build_header(window_width)
        color_palette = _build_color_palette(window_width, drawing_area,
                                             palette_color)

        info_menu, _classification_display = _build_info_menu(
            info_menu_width, body_height, info_menu_color, open_modal, classify_menu.close
        )

        body = FlexBox(window_width, body_height, flex_direction="ROW")
        body.add_children([drawing_area, info_menu])

        base_layer.add_children([header, color_palette, body])

        _result_display = _build_classify_modal(modal_layer, close_modal)

        return classify_menu

    return _setup()
