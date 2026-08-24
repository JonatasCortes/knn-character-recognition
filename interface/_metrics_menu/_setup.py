from . import _constants as const
from functools import partial
from typing import Callable, Final
from desklab import FlexBox, Text, Window, Button
from interface._utils import create_button_with_text, build_header, toggle_brightness_up
from interface._constants import WINDOW_WIDTH, BASE_COLOR, DEFAULT_FONT


metrics_menu: Final[Window] = Window()


def _build_stat_card(spec: const.StatCardSpec, open_modal: Callable[[const.StatCardSpec], None]) -> tuple[Button, Text]:
    card = Button(const.STAT_CARD_WIDTH, const.STAT_CARD_HEIGHT, partial(open_modal, spec),
                  const.STAT_CARD_PADDING,
                  const.STAT_CARD_INNER_SPACE_BETWEEN,
                  corners_radius=const.STAT_CARD_CORNERS_RADIUS,
                  color=spec.accent_color,
                  trigger_actions_on_release=True)
    toggle_brightness_up(card, const.STAT_CARD_BRIGHTNESS_TOGGLE_INTENSITY)
    label_text = Text(spec.label, DEFAULT_FONT.copy(
        size=const.STAT_LABEL_FONT_SIZE), const.STAT_TEXT_COLOR)
    value_text = Text(spec.value, DEFAULT_FONT.copy(
        size=const.STAT_VALUE_FONT_SIZE), const.STAT_TEXT_COLOR)
    card.add_children([label_text, value_text])
    return card, value_text


def _build_stats_grid(open_modal: Callable[[const.StatCardSpec], None]) -> tuple[FlexBox, dict[str, Text]]:
    specs: tuple[const.StatCardSpec, ...] = (
        const.StatCardSpec(const.TRAINING_ACCURACY_LABEL,
                           const.DEFAULT_METRIC_VALUE,
                           const.ACCENT_GREEN,
                           const.TRAINING_ACCURACY_DESCRIPTION),
        const.StatCardSpec(const.USER_ACCURACY_LABEL,
                           const.DEFAULT_METRIC_VALUE,
                           const.ACCENT_BLUE,
                           const.USER_ACCURACY_DESCRIPTION),
        const.StatCardSpec(const.TRAINING_IMAGES_LABEL,
                           const.DEFAULT_METRIC_VALUE,
                           const.ACCENT_ORANGE,
                           const.TRAINING_IMAGES_DESCRIPTION),
        const.StatCardSpec(const.MANUAL_CHECKS_LABEL,
                           const.DEFAULT_METRIC_VALUE,
                           const.ACCENT_PURPLE,
                           const.MANUAL_CHECKS_DESCRIPTION),
        const.StatCardSpec(const.K_VALUE_LABEL,
                           const.DEFAULT_METRIC_VALUE,
                           const.ACCENT_TEAL,
                           const.K_VALUE_DESCRIPTION),
        const.StatCardSpec(const.RECOGNIZED_CHARACTERS_LABEL,
                           const.DEFAULT_METRIC_VALUE,
                           const.ACCENT_TERRACOTTA,
                           const.RECOGNIZED_CHARACTERS_DESCRIPTION),
    )

    row_1 = FlexBox(const.STATS_GRID_WIDTH, const.STAT_CARD_HEIGHT, 0,
                    const.STAT_CARD_SPACE_BETWEEN, "ROW", color=BASE_COLOR)
    row_2 = FlexBox(const.STATS_GRID_WIDTH, const.STAT_CARD_HEIGHT, 0,
                    const.STAT_CARD_SPACE_BETWEEN, "ROW", color=BASE_COLOR)

    value_displays: dict[str, Text] = {}

    for index, spec in enumerate(specs):
        card, value_text = _build_stat_card(spec, open_modal)
        value_displays[spec.label] = value_text
        (row_1 if index < const.STATS_GRID_COLUMNS else row_2).add_children(card)

    grid = FlexBox(const.STATS_GRID_WIDTH, const.STATS_GRID_HEIGHT,
                   0, const.STAT_ROW_SPACE_BETWEEN, color=BASE_COLOR)
    grid.add_children([row_1, row_2])

    return grid, value_displays


def _build_metrics_modal(modal_layer: FlexBox, close_modal: Callable[[], None]) -> Callable[[const.StatCardSpec], None]:
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
        const.CLOSE_MODAL_BUTTON_WIDTH, const.MODAL_HEADER_HEIGHT, const.RETURN_BUTTON_COLOR,
        const.CLOSE_MODAL_BUTTON_TEXT, corners_radius=const.CLOSE_MODAL_BUTTON_CORNERS_RADIUS,
        action=close_modal,
    )

    modal_title = Text("XXXXXXXXXXXXXXXXXXX", DEFAULT_FONT.copy(
        size=const.MODAL_TITLE_FONT_SIZE), "WHITE")
    modal_header.add_children([close_modal_button, modal_title])

    description_container = FlexBox(const.MODAL_CONTENT_WIDTH, const.MODAL_DESCRIPTION_CONTAINER_HEIGHT,
                                    0, const.MODAL_DESCRIPTION_LINE_SPACE_BETWEEN,
                                    corners_radius=const.MODAL_DESCRIPTION_CORNERS_RADIUS,
                                    color=BASE_COLOR.lightened(const.MODAL_CONTENT_CONTAINER_COLOR_LIGHTEN))

    description_lines: tuple[Text, ...] = tuple(
        Text("", DEFAULT_FONT.copy(size=const.MODAL_DESCRIPTION_FONT_SIZE), "WHITE")
        for _ in range(const.MODAL_DESCRIPTION_LINES)
    )
    description_container.add_children(list(description_lines))

    modal_body.add_children(description_container)

    def open_modal(spec: const.StatCardSpec) -> None:
        modal_title.set_text(spec.label)
        for line_text, line in zip(description_lines, spec.description):
            line_text.set_text(line)
        modal_layer.set_visibility(True)

    return open_modal


def metrics_menu_setup() -> Window:
    base_layer = metrics_menu.add_layer()
    modal_layer = metrics_menu.add_layer(color=const.MODAL_OVERLAY_COLOR,
                                         visible=False)

    def close_modal() -> None:
        modal_layer.set_visibility(False)

    header = build_header(WINDOW_WIDTH)
    body = FlexBox(WINDOW_WIDTH, const.BODY_HEIGHT,
                   color=BASE_COLOR.lightened(const.BODY_COLOR_LIGHTEN))

    stats_panel = FlexBox(const.STATS_PANEL_WIDTH, const.STATS_PANEL_HEIGHT, const.STATS_PANEL_PADDING,
                          const.STATS_PANEL_SPACE_BETWEEN,
                          corners_radius=const.STATS_PANEL_CORNERS_RADIUS,
                          color=BASE_COLOR)

    panel_title = Text(const.PANEL_TITLE_TEXT,
                       DEFAULT_FONT.copy(size=const.PANEL_TITLE_FONT_SIZE), "WHITE")

    open_modal = _build_metrics_modal(modal_layer, close_modal)
    stats_grid, _value_displays = _build_stats_grid(open_modal)

    return_button = create_button_with_text(
        int(const.STATS_PANEL_WIDTH /
            const.RETURN_BUTTON_WIDTH_RATIO), const.RETURN_BUTTON_HEIGHT,
        const.RETURN_BUTTON_COLOR, const.RETURN_BUTTON_TEXT,
        corners_radius=const.RETURN_BUTTON_CORNERS_RADIUS,
        font_size=const.RETURN_BUTTON_FONT_SIZE, action=metrics_menu.close,
    )

    stats_panel.add_children([panel_title, stats_grid, return_button])
    body.add_children(stats_panel)

    base_layer.add_children([header, body])
    return metrics_menu
