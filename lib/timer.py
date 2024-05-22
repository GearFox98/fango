import threading
import flet as ft
import time
import lib.libfango as libfango

from lib.translations import TRANSLATIONS
from lib.datasets import Config_File
from lib.datasets import Pomodoro_Timer
from math import pi

class TimerUI(ft.UserControl):
    def __init__(self, page: ft.Page, language: str, pomodoro_timer: Pomodoro_Timer, configuration_file: Config_File, data: dict):
        super().__init__()
        self.page: ft.Page = page
        self.language: str = language
        self.pomodoro_timer: Pomodoro_Timer = pomodoro_timer
        self.configuration_file: Config_File = configuration_file
        self.ui_text: dict = TRANSLATIONS[language]

        self.breaker = threading.Event()
        self.data = data
    
    def build(self):
        # Clock components
        self.clock = ft.Text(value='00:00', text_align=ft.TextAlign.CENTER, size=54)
        self.progress = ft.ProgressRing(value=0.5, rotate=-pi/2, width=300, height=300, stroke_width=30, color=ft.colors.BLUE)
        self.progress_shadow = ft.ProgressRing(value=0.5, rotate=-pi/2, width=300, height=300, stroke_width=30, color=ft.colors.GREY)

        # Stages attributes
        self.loop_label = ft.Text(f"{self.ui_text['STAGES_SECTION'][0]}: 0", size=24)
        self.mode_label = ft.Text(f"{self.ui_text['STAGES_SECTION'][1]}", size=24)

        # Stages (Below the clock)
        self.stages = ft.Row(
            [
                self.loop_label, # Loop Number
                self.mode_label # Mode
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        # Timer component
        return ft.Container(
            ft.Stack(
                [
                    ft.Container(
                        content=self.progress_shadow,
                        width=410,
                        height=330,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=self.progress,
                        width=410,
                        height=330,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Container(height=30),
                                ft.Row([self.clock], alignment=ft.MainAxisAlignment.CENTER),
                                ft.Divider(),
                                self.stages,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        width=410,
                        height=330,
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(35, 50, 35, 0)
                    )
                ]
            )
        )

    # Animation of the progress arc values (Start and end)
    def set_anim_values(self, start: int, end: int, step: int):
        self.start = start
        self.end = end
        self.step = step
    
    # Animate progress
    def anim_progress(self):
        for i in range(self.start, self.end, self.step):
            self.progress.value = (i / 100)/2
            time.sleep(0.005)
            self.page.update()
    
    # Activate daemon break
    def set_breaker(self, _e):
        if self.data['run'] == False:
            self.set_anim_values(100, -1, -1)
            self.anim_progress()
            self.breaker.clear()
            self.data['run'] = True
            #self.main_button.icon = ft.icons.STOP
            #self.main_button.text = self.ui_text["BUTTONS"][1]
            t = threading.Thread(
                target=libfango.timer,
                args=[self.page, self.clock, self.progress, self.mode_label, self.loop_label, self.breaker],
                daemon=True,
                name="Timer")
            t.start()
            print(f"Started thread: {t.name}")
        else:
            self.data["run"] = False
            #self.main_button.icon = ft.icons.PLAY_ARROW
            #self.main_button.text = f"{self.ui_text['BUTTONS'][0]}"
            self.breaker.set()
            self.page.update()