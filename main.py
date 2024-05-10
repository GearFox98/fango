import os, threading
import flet as ft
import lib.main_ui as ui
import lib.libfango as libfango

data = {
    'clock' : '00:00',
    'mode' : 0,
    'run' : False
}

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
                args=[page, ui.clock, ui.progress, ui.mode_label, ui.loop_label, breaker],
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

    # Main UI "static" elements
    main_button = ft.TextButton(
        text="Iniciar",
        icon=ft.icons.PLAY_ARROW,
        icon_color=ft.colors.BLACK,
        on_click=set_breaker
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
        on_click=lambda _: page.go("/store")
    )

    appbar = ft.AppBar(
        title=ft.Text(libfango.APP_NAME, weight=ft.FontWeight.BOLD),
        actions=[
            main_button,
            option_button
        ]
    )

    # Animate progress
    def anim_progress(start: int, end: int, step: int):
        for i in range(start, end, step):
            ui.progress.value = (i / 100)/2
            ui.time.sleep(0.005)
            page.update()

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ui.appbar,
                    ui.timer
                ],
            )
        )
        if page.route == "/store":
            page.views.append(
                ft.View(
                    "/store",
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


ft.app(target=main)