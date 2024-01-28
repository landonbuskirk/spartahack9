import reflex as rx
from webui.state import State


def modal() -> rx.Component:
    """A modal to create a new chat."""
    return rx.modal(
        rx.modal_overlay(
            rx.modal_content(
                rx.modal_header(
                    rx.hstack(
                        rx.text("Create new chat"),
                        rx.icon(
                            tag="close",
                            font_size="sm",
                            on_click=State.toggle_modal,
                            color="#fff8",
                            _hover={"color": "#fff"},
                            cursor="pointer",
                        ),
                        align_items="center",
                        justify_content="space-between",
                    )
                ),
                rx.modal_body(
                    rx.input(
                        placeholder="Type something...",
                        border_color="lime",
                        on_blur=State.set_new_chat_name,
                        bg="#222",
                        
                        _placeholder={"color": "#fffa"},
                    ),
                ),
                rx.modal_footer(
                    rx.button(
                        "Create",
                        color="#627b3a",
                        bg_color="var(--accent-9)",
                        box_shadow="md",
                        px="4",
                        py="2",
                        h="auto",
                        _hover={"bg": "white"},
                        on_click=State.create_chat,
                    ),
                ),
                bg="#222",
                color="#fff",
            ),
        ),
        is_open=State.modal_open,
    )
