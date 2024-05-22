import flet as ft
import lib.libfango as libfango

from lib.translations import TRANSLATIONS

class MainAppbar(ft.AppBar):
    def __init__(self, page: ft.Page, lang: str, pomodoro_data: dict, set_breaker):
        super().__init__()
        self.page = page
        self.ui_text: dict = TRANSLATIONS[lang]
        self.pomodoro_data: dict = pomodoro_data

        self.set_breaker = set_breaker
    
    def build(self):
        main_button = ft.TextButton(
            text=f"{self.ui_text['BUTTONS'][0]}",
            icon=ft.icons.PLAY_ARROW,
            on_click=self.set_breaker
        )

        option_button = ft.TextButton(
            content=ft.Row(
                [
                    ft.Icon(
                        name=ft.icons.SETTINGS,
                    )
                ]
            ),
            width=50,
            on_click=self.opt_btn_func
        )
        # App menu
        return ft.AppBar(
            title=ft.Text(libfango.APP_NAME, weight=ft.FontWeight.BOLD),
            actions=[
                main_button,
                option_button
            ],
            #bgcolor=ft.colors.SURFACE_VARIANT
        )
    
    def opt_btn_func(self, _e):
            self.page.go("/conf") # type: ignore