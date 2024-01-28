"""The main Chat app."""

import reflex as rx

from webui import styles
from webui.components import chat, modal, navbar, sidebar
from webui.state import State
import reflex.components.radix.themes as rdxt

@rx.page()
def index() -> rx.Component:
    """The main app."""
    return rx.vstack(
        navbar(), 
        chat.chat(),
        chat.action_bar(),
        sidebar(),
        modal(),
        color=styles.text_light_color,
        min_h="100vh",
        align_items="stretch",
        spacing="0",
        bg="#272727"
    )

@rx.page()
def stats() -> rx.Component:
    return rx.vstack(
        navbar(),
        bg="#272727"
    )

style = {
    "font_family": "LufgaRegular",  # Replace with your chosen font family
}
# Add state and page to the app.
app = rx.App(
    stylesheets=["styles.css","fonts.css"],
    overlay_component=None,
    theme=rdxt.theme(
        appearance="dark",
        has_background=True,
        radius="none",
        accent_color="lime",
    style=style    
    ),
)
