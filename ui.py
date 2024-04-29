import flet as ft
import asyncio

async def main(page: ft.Page):
    page.title = "Fango"
    page.window_max_height = 415
    page.window_max_width = 415
    page.window_min_height = 415
    page.window_min_width = 415
    page.window_maximizable = False

    page.appbar = ft.AppBar(
        title=ft.Text("Fango"),
        actions=[
            ft.TextButton(text="Iniciar", icon=ft.icons.PLAY_ARROW, icon_color=ft.colors.BLACK),
            ft.TextButton(content=ft.Row([
                ft.Icon(name=ft.icons.SETTINGS,
                        color=ft.colors.BLACK)
                        ]),
                width=50)
        ]
    )

    TIMER = ft.Container(content = ft.Row(
            [
                ft.Text("Placeholder")
            ]),
        padding=3,
        width=410,
        height=330,
        bgcolor=ft.colors.BLUE)

    await page.add_async(TIMER)

asyncio.run(ft.app_async(target=main))