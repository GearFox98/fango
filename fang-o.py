import threading
import flet as ft
import os, time
import lib.libfango as libfango
import lib.opt as opt

from math import pi

data = {
    'clock' : '00:00',
    'mode' : 0,
    'run' : False
}

# Debugging
def options(_e):
    libfango.notifier("It works!", "Sound!")

# Main UI
async def main(page: ft.Page):
    page.title = libfango.APP_NAME
    page.window_width = 415
    page.window_height = 415
    page.window_max_height = 400
    page.window_max_width = 415
    page.window_min_height = 400
    page.window_min_width = 415
    page.window_maximizable = False
    page.padding = 0

    # MAIN PAGE
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

    # Animate progress
    def anim_progress(start: int, end: int, step: int):
        for i in range(start, end, step):
            progress.value = (i / 100)/2
            time.sleep(0.005)
            page.update()

    # Threaded Functions
    # moved to lib/libfango.py
    # To cancel the process
    breaker = threading.Event()

    # Main function
    # Activate daemon break
    def set_breaker(_e):
        if data['run'] == False:
            anim_progress(100, -1, -1)
            breaker.clear()
            data['run'] = True
            main_button.icon = ft.icons.STOP
            main_button.text = "Detener"
            t = threading.Thread(
                target=libfango.timer,
                args=[page, clock, progress, mode_label, loop_label, breaker],
                daemon=True,
                name="Timer")
            t.start()
            print(f"Started thread: {t.name}")
        else:
            data["run"] = False
            main_button.icon = ft.icons.PLAY_ARROW
            main_button.text = "Iniciar"
            breaker.set()
            page.update()

    # UI
    main_button = ft.TextButton(
        text="Iniciar",
        icon=ft.icons.PLAY_ARROW,
        icon_color=ft.colors.BLACK,
        on_click=set_breaker
    )

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
        on_click=lambda _: page.go("/conf")
    )

    # App menu
    appbar = ft.AppBar(
        title=ft.Text(libfango.APP_NAME, weight=ft.FontWeight.BOLD),
        actions=[
            main_button,
            option_button
        ]
    )

    # CONFIG
    # Counters
    work_counter = opt.work_counter
    free_counter = opt.free_counter
    lfree_counter = opt.lfree_counter

    # Other opts
    stats = opt.stats
    lang = opt.lang

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    appbar,
                    timer
                ],
            )
        )
        if page.route == "/conf":
            page.views.append(
                ft.View(
                    "/conf",
                    [
                        ft.AppBar(title=ft.Text("Store"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

    page.add(timer)

# Create config folder
if not os.path.exists(os.path.expanduser("~/.fango")):
    os.mkdir(os.path.expanduser("~/.fango"))

ft.app(target=main)
