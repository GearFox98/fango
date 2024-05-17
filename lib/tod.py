import os, json
from sqlite3 import Row
from typing import Text
import flet as ft
import lib.libfango as libfango

from lib.translations import TRANSLATIONS
from lib.datasets import Task

class TaskControl(ft.UserControl):
    # Each task has Name, Details, a Deadline and can be Done or not (by default they're not done: False)
    def __init__(self, name: str, details: str | None = None, deadline: None = None, done: bool = False, task_status_change, task_delete) -> None: #type:ignore
        super().__init__()
        self.name = name
        self.details = details
        self.deadline = deadline
        self.done = done
        self.task_status_change = task_status_change
        self.task_delete = task_delete

        #self.data = Task(name, details, deadline, done)
    
    def build(self):
        self.title = ft.Text(
            value=self.name,
            weight=ft.FontWeight.BOLD,
            size=24
        )

        self.description = ft.Text(
            value=self.details
        )

        self.deadline_indicator = ft.Row(
            controls=[
                ft.Icon(ft.icons.CALENDAR_TODAY),
                ft.Text(value=self.deadline)
            ]
        )

        self.done_check = ft.Checkbox(
            #label=self.name,
            value=False,
            on_change=self.change_done
        )

        self.view_task = ft.IconButton(
            icon=ft.icons.LOOKS
        )

        self.display_task = ft.Row(
            controls=[
                self.done_check,
                self.title,
                ft.Row(
                    controls=[
                        self.view_task
                    ]
                )
            ]
        )

    async def change_done(self, e):
        self.completed = self.done_check.value
        await self.task_status_change(self)

    async def delete_clicked(self, e):
        await self.task_delete(self)

class TodoView(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.conf = libfango.Config_File()
        self.ui_text = TRANSLATIONS[self.conf.lang]['TODO']

        # TODO - Load saved tasks

    def build(self):
        self.deadline_label = ft.Text(value="No deadline")

        self.new_task = ft.TextField(
            label=self.ui_text[0],
            expand=True,
            #on_submit=
        )

        self.tasks = ft.Column()
    
        self.filter = ft.Tabs(
                scrollable=False,
                selected_index=0,
                #on_change=self.tabs_changed,
                tabs=[ft.Tab(text=self.ui_text[1]), ft.Tab(text=self.ui_text[2]), ft.Tab(text=self.ui_text[3]), ft.Tab(text=self.ui_text[4])],
            )
        
        return ft.Column(
            width=600,
            controls=[
                ft.Row(
                    controls=[
                        self.new_task,
                        ft.FloatingActionButton(
                            icon=ft.icons.ADD,
                            #on_click=self.add_clicked
                        ),
                    ],
                ),
                ft.Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.tasks,
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                #self.items_left,
                                ft.OutlinedButton(
                                    text="Clear completed", #on_click=self.clear_clicked
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )