import flet as ft
import lib.libfango as libfango

from math import pi

# CLock view
clock = ft.Text(value='00:00', text_align=ft.TextAlign.CENTER, size=54)
progress = ft.ProgressRing(value=0.5, rotate=-pi/2, width=300, height=300, stroke_width=30, color=ft.colors.BLUE)
progress_shadow = ft.ProgressRing(value=0.5, rotate=-pi/2, width=300, height=300, stroke_width=30, color=ft.colors.GREY)

# Stages attributes
loop_label = ft.Text("Sesión: 0", size=24)
mode_label = ft.Text("Trabajo", size=24)

 # Stages (Below the clock)
stages = ft.Row(
    [
        loop_label, # Loop Number
        mode_label # Mode
    ],
    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
)

# Timer component
timer = ft.Container(
    ft.Stack(
        [
            ft.Container(
                content=progress_shadow,
                width=410,
                height=330,
                alignment=ft.alignment.center
            ),
            ft.Container(
                content=progress,
                width=410,
                height=330,
                alignment=ft.alignment.center
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(height=30),
                        ft.Row([clock], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Divider(),
                        stages,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    
                ),
                width=410,
                height=330,
                alignment=ft.alignment.center,
                padding=35
            )
        ]
    )
)

# UI
main_button = ft.TextButton(
    text="Iniciar",
    icon=ft.icons.PLAY_ARROW,
    icon_color=ft.colors.BLACK,
    #on_click=set_breaker
)

# TODO - Options view
option_button = ft.TextButton(
    content=ft.Row(
        [
            ft.Icon(
                name=ft.icons.SETTINGS,
                color=ft.colors.BLACK
            )
        ]
    ),
    width=50,
    #on_click=options
)

# App menu
appbar = ft.AppBar(
    title=ft.Text(libfango.APP_NAME, weight=ft.FontWeight.BOLD),
    actions=[
        main_button,
        option_button
    ]
)