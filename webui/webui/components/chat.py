import reflex as rx

from webui import styles
from webui.components import loading_icon
from webui.state import QA, State


def message(qa: QA) -> rx.Component:
    """A single question/answer message.

    Args:
        qa: The question/answer pair.

    Returns:
        A component displaying the question/answer pair.
    """
    return rx.box(
        rx.box(
            rx.text(
                qa.question,
                bg="white",
                shadow=styles.shadow_light,
                **styles.message_style,
            ),
            text_align="right",
            margin_top="1em",
            padding_top="3em",
        ),
        rx.box(
            rx.text(
                qa.answer,
                bg="var(--accent-9)",
                shadow=styles.shadow_light,
                **styles.message_style,

            ),
            text_align="left",
            padding_top="3em",
        ),
        width="100%",
    )


def chat() -> rx.Component:
    """List all the messages in a single conversation."""
    return rx.vstack(
        rx.box(rx.foreach(State.chats[State.current_chat], message)),
        py="8",
        flex="1",
        width="100%",
        padding_x="4",
        align_self="center",
        overflow="hidden",
        padding_bottom="5em",
        padding_top="5em",
    )





def action_bar() -> rx.Component:
    '''
    """The action bar to send a new message."""
    return rx.box(
    rx.hstack(
        rx.text("Elixr 1.0", style={"color": "gray"}),
        rx.icon(tag="chevron_down", style={"color": "gray"}),
        rx.form(
            rx.form_control(
                rx.hstack(
                    rx.input(
                        placeholder="Type something...",
                        id="question",
                        bg="#f3f4f6",
                        _placeholder={"color": "#d7d9db"},
                    ),
                    rx.button(
                        rx.cond(
                            State.processing,
                            rx.icon(tag="loading"),  # Assuming 'loading' is a valid icon tag
                            rx.text("Send"),
                        ),
                        type_="submit",
                        style={"bg": "#f3f4f6", "color": "gray", "border": "none"},
                    ),
                ),
                is_disabled=State.processing,
            ),
            on_submit=State.process_question,
            reset_on_submit=True,
        ),
    ),
    style={
        "position": "fixed",
        "bottom": "25%",  # Adjusted to place in the bottom half of the screen
        "left": "50%",
        "transform": "translateX(-50%)",
        "width": "50%",
        "max_width": "500px",  # Ensures the box doesn't become too wide
        "border_radius": "9999px",  # Pill shape
        "box_shadow": "0 2px 4px rgba(0, 0, 0, 0.1)",  # Floating effect
        "padding": "1em",
        "align_items": "center",
        "justify_content": "center",
        "gap": "1rem",
        "z_index": "10",  # Ensure it's above other content
    }
)
''' 
    return rx.hstack(
    rx.box(
        style={"width": "250px"}  # Fixed width of the left-most box
    ),
    # Reduced spacer or remove the spacer if needed
    # You can remove this spacer if necessary
    rx.box(
        rx.vstack(
            rx.form(
                rx.form_control(
                    rx.hstack(
                        rx.input(
                            placeholder="Type something...",
                            id="question",
                            _placeholder={"color": "#272727"},
                            _hover={"border_color": styles.accent_color},
                            color="#3d3d3d",
                            style=styles.input_style,
                            width="100%"
                        ),
                        rx.button(
                            "Send",
                            type_="submit",
                            bg_color="var(--accent-9)",
                            _hover={"bg": styles.accent_color},
                            style=styles.input_style,
                        ),
                        justify="start",  # Ensure button sticks to end of input
                    ),
                    is_disabled=State.processing,
                ),
                on_submit=State.process_question,
                reset_on_submit=True,
                width="100%",
            ),
            width="100%",
        ),
        flex="2",  # Allows the box to grow, taking up more space
        padding="2px",
    ),
    width="100%",
    bottom="10px",
    left="0px",
    position="fixed",
    justify="center",
    z_index="1",
    padding="1em",
)
'''
    return rx.box(
        rx.hstack(
            rx.box(
                style={"size":"250px"}
            ),
            rx.spacer(),
            rx.box(
            rx.vstack(
                        rx.form(
                            rx.form_control(
                                rx.hstack(
                                    rx.input(
                                        placeholder="Type something...",
                                        id="question",
                                        bg="#f3f4f6",
                                        _placeholder={"color": "#d7d9db"},
                                        _hover={"border_color": styles.accent_color},
                                        color ="black"
                                    ),
                                    rx.button(
                                        rx.cond(
                                            State.processing,
                                            loading_icon(height="1em"),
                                            rx.text("Send"),
                                        ),
                                        type_="submit",
                                        _hover={"bg": styles.accent_color},
                                    ),
                                ),
                                is_disabled=State.processing,
                            ),
                            on_submit=State.process_question,
                            reset_on_submit=True,
                            width="100%",
                        ),
                        width="100%",
                        max_w="3xl",
                        mx="auto",
                    ),
            ),
                    rx.spacer(),
                style={"align_items": "center", "gap": "0.5rem"}
                
        ),
        style={
            "max_width": "40rem",  # Adjust the maximum width as needed
            "border_radius": "9999px",  # Creates the pill shape
            "box_shadow": "0 4px 8px rgba(0, 0, 0, 0.2)",  # More prominent and longer shadow
            "padding": "1rem",
            "margin": "0 auto",
            "display": "flex",
            "justify_content": "space-between",  # This will position additional components to the right
            "position": "fixed",
            "bottom": "5%",
            "transform": "translateX(-50%)",
            "background_color": "#FFF",
            "z_index": "10",
        }
)
'''