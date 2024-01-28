import reflex as rx

bg_dark_color = "#fafafa"
bg_medium_color = "#fafafa"

border_color = "#fff3"

accennt_light = "#6649D8"
accent_color = "#c7ed77"
accent_dark = "#4c2db3"

icon_color = "#919191"

text_light_color = "#fff"
shadow_light = "rgba(17, 12, 46, 0.15) 0px 48px 100px 0px;"
shadow = "rgba(50, 50, 93, 0.25) 0px 50px 100px -20px, rgba(0, 0, 0, 0.3) 0px 30px 60px -30px, rgba(10, 37, 64, 0.35) 0px -2px 6px 0px inset;"

message_style = dict(display="inline-block", p="4", border_radius="xl", max_w="60em", color="black")

input_style = dict(
    bg=bg_medium_color,
    border_color=border_color,
    border_width="1px",
    p="4",
    color="black"
)

icon_style = dict(
    font_size="md",
    color=icon_color,
    _hover=dict(color=text_light_color),
    cursor="pointer",
    w="8",
)

sidebar_style = dict(
    border="double 1px transparent;",
    border_radius="10px;",
    background_image=f"linear-gradient({bg_dark_color}, {bg_dark_color}), radial-gradient(circle at top left, {accent_color},{accent_dark});",
    background_origin="border-box;",
    background_clip="padding-box, border-box;",
    p="2",
    _hover=dict(
        background_image=f"linear-gradient({bg_dark_color}, {bg_dark_color}), radial-gradient(circle at top left, {accent_color},{accennt_light});",
    ),
)

base_style = {
    rx.Avatar: {
        "shadow": shadow,
        "color": "blue",
        "bg": border_color,
    },
    rx.Menu: {
        "bg": bg_dark_color,
        "border": f"red",
    },
    rx.MenuList: {
        "bg": bg_dark_color,
        "border": f"1.5px solid {bg_medium_color}",
    },
    rx.MenuDivider: {
        "border": f"1px solid {bg_medium_color}",
    },
    rx.MenuItem: {
        "bg": bg_dark_color,
        "color": text_light_color,
    },
    rx.DrawerContent: {
        "bg": "#fafafa",
        "color": text_light_color,
        "opacity": "0.9",
    },
    rx.Hstack:{
        "bg": "fafafa",
        "align_items": "center",
        "justify_content": "space-between",
    },
    rx.Vstack: {
"        bg": "fafafa",
        "align_items": "stretch",
        "justify_content": "space-between",
    },
}
