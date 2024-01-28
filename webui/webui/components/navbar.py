import asyncio
import datetime
import reflex as rx

from webui import styles
from webui.state import State
import reflex.components.radix.themes as rdxt


class DateState(rx.State):
    current_date: str = datetime.datetime.now().strftime("%d, %B %Y")

    @rx.background
    async def update_date(self):
        while True:
            async with self:
                self.current_date = datetime.datetime.now().strftime("%d, %B %Y")
            await asyncio.sleep(1)


def navbutton(label, route):
    return rdxt.button(
        rdxt.link(label, href=route),
        radius="full",
        size="4",
        background_color=rx.cond(
            route == rx.State.router.page.path,
            "var(--accent-12)",
            "var(--accent-9)",
        ),
    )

def navbar():
    
    return rx.hstack(
        rdxt.box(
            rx.box(style={'width': '250px'}),
        ),
        rx.spacer(),
        rdxt.box(
            navbutton("PAM", "/"),
            navbutton("Stats", "/stats"),
            spacing="0",
            background_color="var(--accent-9)",
            border_radius="999999px",
            padding="1px",
            
        ),
        rx.spacer(),
        rx.button(
            "+ New chat",
            color="#627b3a",
            bg_color="var(--accent-9)",
            size="lg",
            padding="3px",
            
            on_click=State.toggle_modal,
                ),
        width="100%",
        top="3px",
        left="0px",
        position="fixed",
        justify="space-between",
        align_items="center",
        z_index="1",
        padding="1em",
    )

'''
def navbar():
    return rx.hstack(
        rx.spacer(),
        rdxt.box(
            navbutton("Albert", "/"),
            navbutton("Stats", "/stats"),
            spacing="0",
            background_color="var(--accent-9)",
            border_radius="9999px",
            
        ),
        rx.spacer(),
        rx.button(
            "+ New chat",
            bg=styles.accent_color,
            px="4",
            py="2",
            h="auto",
            on_click=State.toggle_modal,
                ),
        width="100%",
        top="3px",
        position="fixed",
        justify="space-between",
        align_items="center",
    )
'''
'''
    return rx.box(
        rx.hstack(
            rx.button(
                rx.breadcrumb(
                    
                ),
            ),
        ),
        position="fixed",
        bg="gray",
        z_index="1",
    )
'''