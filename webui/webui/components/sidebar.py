import reflex as rx
import reflex.components.radix.themes as rdxt
from webui import styles
from webui.state import State

class IconState(rx.State):
    hover: bool = False

    def on_hover(self):
        self.hover = True

    def on_leave(self):
        self.hover = False



def sidebar_chat(chat: str) -> rx.Component:
    """A sidebar chat item.

    Args:
        chat: The chat item.
    """
    return rx.box(
    rx.vstack(
    rx.hstack(
        rx.center(
            chat,
            on_click=lambda: State.set_chat(chat),
            width="140px",
            color="white",
            bg_color="transparent",
            flex="1",
            border_radius="20px",
            _hover={
                "bg_color": "white",
                "color": "gray",  # Text color changes to gray on hover
                "box_shadow": "0 0 8px 2px rgba(0,0,0,0.2)",
            },
        ),
        rx.box(
            rx.icon(
                tag="delete",
                on_click=State.delete_chat,
                width="2em",
                padding="2px",
                height="auto",
                border_radius="20px",
                _hover={
                    "color": "gray",  # Icon color changes to gray on hover
                    "bg_color": "white",  # Background color changes to white on hover
                },
            ),
            border_radius="20px"
        ),
        border_radius="20px",
        cursor="pointer",
        padding="2px",
    ),
    
    bg_color="transparent",
    width="240px",
    border_radius="20px",
    
    ),
    )

def sidebar():
    return rx.box(
        rx.vstack(
            rx.image(
                src="/pam.png",  # Updated src path if "green.png" is in the assets folder
                width="240px",
                height="auto",
                border_radius="20%",
                pt="10px",
            ),
            rx.center(
                rx.text("Chats", font_size="1.25em", color="#5c5c5c"),
                bg_color="white",
                border_radius="20px",
                width="240px",
                align_items="center",
                padding="2px,"
            ),
            rx.box(
                style={"height":"1em"}
            ),
            rx.vstack(
                rx.foreach(State.chat_titles, lambda chat: sidebar_chat(chat)),
                
                align_items="stretch",
            ),
        ),
        background_color="#3d3d3d",
        width="250px",
        position="fixed",
        height="100%",
        left="0px",
        top="0px",
        z_index="5",
    )
    '''
    return rx.box(
        rx.vstack(
            rx.image(
                src="/green.png",width="230px",height="auto",border_radius="20%",pt="20px"
            ),
            rx.box(
                    rx.text("Chats",font_size="2em",color="#4b6c3a"),
                    bg_color="#394021",
                    border_radius="9999px",
                    ),
            rx.vstack(
                rx.foreach(State.chat_titles, lambda chat: sidebar_chat(chat)),
                align_items="stretch",
            ),
        background_color="#3d3d3d",  # Set the background color for the sidebar
        width="250px",
        position="fixed",
        height="100%",
        left="0px",
        top="0px",
        z_index="5",  # Ensures the sidebar overlays other content
            ),
        ),
        '''