import reflex as rx
from webui import styles
from webui.state import State

def newchat():
    return rx.button(
                    "+ New chat",
                    bg=styles.accent_color,
                    px="4",
                    py="2",
                    h="auto",
                    on_click=State.toggle_modal,
                    top="2px",
                    right="2px",
                ),