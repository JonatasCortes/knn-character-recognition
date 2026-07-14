from . import _constants as const
from functools import partial
from typing import Any, Callable
from desklab import Button, Color, DrawingArea, FlexBox, Font, Text, Window
from src.interface._constants import WINDOW_HEIGHT, WINDOW_WIDTH, BASE_COLOR, HEADER_HEIGHT
from src.interface._utils import (create_button_with_image, toggle_brightness_up,
                                  create_button_with_text, build_header)


def _create_display_box(width: int, height: int, color: Color | str | tuple[int, ...], text: str, font: Font, corners_radius: int | tuple[int, int, int, int] = const.CLASSIFICATION_DISPLAY_CORNERS_RADIUS,) -> FlexBox:
    display = FlexBox(width, height,
                      corners_radius=corners_radius,
                      color=color)
    display.add_children(Text(text, font, "WHITE"))
    return display


def _build_color_palette(width: int, drawing_area: DrawingArea, palette_color: Color) -> FlexBox:
    color_palette = FlexBox(width, const.COLOR_PALETTE_HEIGHT, 0,
                            const.COLOR_PALETTE_SPACE_BETWEEN, "ROW",
                            color=palette_color)

    for color, emphasis_intensity in const.BRUSH_COLORS:
        brush_button = Button(const.BRUSH_BUTTON_SIZE, const.BRUSH_BUTTON_SIZE,
                              corners_radius=const.BRUSH_BUTTON_CORNERS_RADIUS, color=color)
        toggle_brightness_up(brush_button, emphasis_intensity)
        brush_button.add_actions(
            partial(drawing_area.set_brush_color, color))
        color_palette.add_children(brush_button)

    tool_actions: tuple[Callable[..., Any], ...] = (drawing_area.draw, drawing_area.fill,
                                                    drawing_area.erase, drawing_area.clear)
    color_palette.add_children(
        [
            create_button_with_image(f"{const.ASSETS_PATH}{icon}", const.TOOL_BUTTON_SIZE,
                                     const.TOOL_BUTTON_SIZE, palette_color, action)
            for icon, action in zip(const.TOOL_ICONS, tool_actions)
        ]
    )
    return color_palette


def _build_info_menu(width: int, height: int, color: Color, on_classify: Callable[[], Any], on_return: Callable[[], Any],) -> tuple[FlexBox, FlexBox]:
    info_menu = FlexBox(width, height, const.INFO_MENU_PADDING, const.INFO_MENU_SPACE_BETWEEN,
                        color=color, vertical_alignment="BOTTOM")

    classification_display = _create_display_box(
        int(width / const.CLASSIFICATION_DISPLAY_WIDTH_RATIO),
        int(height / const.CLASSIFICATION_DISPLAY_HEIGHT_RATIO),
        color.lightened(const.CLASSIFICATION_DISPLAY_COLOR_LIGHTEN),
        const.CLASSIFICATION_DISPLAY_DEFAULT_TEXT, const.DISPLAY_FONT,
    )
    buttons_container = FlexBox(
        int(width / const.BUTTONS_CONTAINER_WIDTH_RATIO),
        int(height / const.BUTTONS_CONTAINER_HEIGHT_RATIO),
        space_between=const.BUTTONS_CONTAINER_SPACE_BETWEEN,
        corners_radius=const.BUTTONS_CONTAINER_CORNERS_RADIUS,
        color=BASE_COLOR.lightened(const.BUTTONS_CONTAINER_COLOR_LIGHTEN),
    )
    button_width = int(width / const.ACTION_BUTTON_WIDTH_RATIO)
    button_height = int(height / const.ACTION_BUTTON_HEIGHT_RATIO)

    specs: tuple[const.ActionButtonSpec, ...] = (
        const.ActionButtonSpec("CLASSIFY", const.CORRECT_COLOR,
                               const.CLASSIFY_BUTTON_CORNERS_RADIUS, on_classify),
        const.ActionButtonSpec("RETURN", const.INCORRECT_COLOR,
                               const.RETURN_BUTTON_CORNERS_RADIUS, on_return),
    )
    for spec in specs:
        buttons_container.add_children(
            create_button_with_text(
                button_width, button_height, spec.color, spec.text,
                corners_radius=spec.corners_radius, action=spec.action,
            )
        )

    info_menu.add_children([classification_display, buttons_container])
    return info_menu, classification_display


def _build_classify_modal(modal_layer: FlexBox, close_modal: Callable[[], Any]) -> FlexBox:

    modal_background = FlexBox(const.MODAL_WIDTH, const.MODAL_HEIGHT, corners_radius=20,
                               color=BASE_COLOR.lightened(const.MODAL_BACKGROUND_COLOR_LIGHTEN))

    modal_layer.add_children(modal_background)

    modal_header = FlexBox(const.MODAL_WIDTH, const.MODAL_HEADER_HEIGHT, 0, const.MODAL_HEADER_SPACE_BETWEEN,
                           "ROW", "LEFT", corners_radius=(20, 20, 0, 0),
                           color=BASE_COLOR.lightened(const.MODAL_HEADER_COLOR_LIGHTEN))

    modal_body = FlexBox(const.MODAL_WIDTH, const.MODAL_BODY_HEIGHT, const.MODAL_BODY_PADDING, const.MODAL_BODY_SPACE_BETWEEN,
                         corners_radius=(0, 0, 20, 20),
                         color=BASE_COLOR.lightened(const.MODAL_BACKGROUND_COLOR_LIGHTEN))

    modal_background.add_children([modal_header, modal_body])

    close_modal_button = create_button_with_text(
        const.CLOSE_MODAL_BUTTON_WIDTH, const.MODAL_HEADER_HEIGHT, const.INCORRECT_COLOR,
        const.CLOSE_MODAL_BUTTON_TEXT, corners_radius=const.CLOSE_MODAL_BUTTON_CORNERS_RADIUS,
        action=close_modal,
    )

    modal_title = Text(const.MODAL_TITLE_TEXT,
                       const.DEFAULT_FONT.copy(
                           size=const.MODAL_TITLE_FONT_SIZE),
                       "WHITE")
    modal_header.add_children([close_modal_button, modal_title])

    result_display = _create_display_box(
        const.MODAL_CONTENT_WIDTH, const.RESULT_DISPLAY_HEIGHT,
        BASE_COLOR.lightened(const.RESULT_DISPLAY_COLOR_LIGHTEN),
        const.RESULT_DISPLAY_DEFAULT_TEXT, const.DISPLAY_FONT,
        corners_radius=const.RESULT_DISPLAY_CORNERS_RADIUS,
    )

    verdict_buttons = FlexBox(
        const.MODAL_CONTENT_WIDTH, const.VERDICT_CONTAINER_HEIGHT, const.VERDICT_BUTTONS_PADDING,
        const.VERDICT_BUTTON_SPACE_BETWEEN, "ROW", corners_radius=const.VERDICT_BUTTONS_CORNERS_RADIUS,
        color=BASE_COLOR.lightened(const.VERDICT_BUTTONS_COLOR_LIGHTEN),
    )

    verdict_button_width = (
        const.MODAL_CONTENT_WIDTH - 2 * const.VERDICT_BUTTONS_PADDING -
        const.VERDICT_BUTTON_SPACE_BETWEEN
    ) // 2

    verdict_buttons.add_children(
        [
            create_button_with_text(
                verdict_button_width, const.VERDICT_BUTTON_HEIGHT, const.CORRECT_COLOR,
                const.VERDICT_CORRECT_TEXT, corners_radius=const.VERDICT_CORRECT_CORNERS_RADIUS,
                font_size=const.VERDICT_BUTTON_FONT_SIZE,
            ),
            create_button_with_text(
                verdict_button_width, const.VERDICT_BUTTON_HEIGHT, const.INCORRECT_COLOR,
                const.VERDICT_INCORRECT_TEXT, corners_radius=const.VERDICT_INCORRECT_CORNERS_RADIUS,
                font_size=const.VERDICT_BUTTON_FONT_SIZE,
            ),
        ]
    )

    modal_body.add_children([result_display, verdict_buttons])
    return result_display


def classify_menu_setup() -> Window:

    drawing_area_width = int(WINDOW_WIDTH / const.DRAWING_AREA_WIDTH_RATIO)
    info_menu_width = WINDOW_WIDTH - drawing_area_width
    body_height = WINDOW_HEIGHT - HEADER_HEIGHT - const.COLOR_PALETTE_HEIGHT

    info_menu_color = BASE_COLOR.lightened(const.MODAL_HEADER_COLOR_LIGHTEN)
    palette_color = BASE_COLOR.lightened(const.BUTTONS_CONTAINER_COLOR_LIGHTEN)

    classify_menu = Window()
    base_layer = classify_menu.add_layer()
    modal_layer = classify_menu.add_layer(
        color=const.MODAL_OVERLAY_COLOR, visible=False)

    def open_modal() -> None:
        modal_layer.set_visibility(True)

    def close_modal() -> None:
        modal_layer.set_visibility(False)

    drawing_area = DrawingArea(drawing_area_width, body_height, const.DRAWING_AREA_PADDING,
                               BASE_COLOR.lightened(
                                   const.DRAWING_AREA_COLOR_LIGHTEN),
                               eraser_width=const.DRAWING_AREA_ERASER_WIDTH)

    header = build_header(WINDOW_WIDTH)
    color_palette = _build_color_palette(
        WINDOW_WIDTH, drawing_area, palette_color)

    info_menu, _classification_display = _build_info_menu(
        info_menu_width, body_height, info_menu_color, open_modal, classify_menu.close
    )

    body = FlexBox(WINDOW_WIDTH, body_height, flex_direction="ROW")
    body.add_children([drawing_area, info_menu])

    base_layer.add_children([header, color_palette, body])

    _result_display = _build_classify_modal(modal_layer, close_modal)

    return classify_menu
