import flet as ft
import lib.main_ui as ui
import lib.libfango as libfango

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

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ui.appbar,
                    ft.ElevatedButton("Visit Store", on_click=lambda _: page.go("/store")),
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