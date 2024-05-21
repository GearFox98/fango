import os, json
import flet as ft
import lib.libfango as libfango

from lib.translations import TRANSLATIONS
from lib.datasets import Task

class TaskControl(ft.UserControl):
    # Each task has Name, Details, a Deadline and can be Done or not (by default they're not done: False)
    def __init__(self, name: str, task_status_change, task_delete, details: str | None = None, deadline: None = None, done: bool = False) -> None: #type:ignore
        super().__init__()
        self.name: str = name
        self.details: str | None = details
        self.deadline = deadline
        self.done: bool = done
        self.task_status_change = task_status_change
        self.task_delete = task_delete

        #self.data = Task(name, details, deadline, done)
    
    def build(self):
        self.title = ft.Text(
            value=self.name,
            weight=ft.FontWeight.BOLD,
            size=24
        )
        self.edit_name = ft.TextField(expand=1)

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
            on_change=self.status_changed
        )

        self.view_task = ft.IconButton(
            icon=ft.icons.REMOVE_RED_EYE,
            tooltip="See all task details"
        )

        self.edit_button = ft.IconButton(
            icon=ft.icons.EDIT,
            tooltip="Edit"
        )

        self.display_view = ft.Row(
            controls=[
                self.done_check,
                self.title,
                ft.Row(
                    controls=[
                        self.view_task,
                        self.edit_button,
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            on_click=self.delete_clicked
                        )
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=self.save_clicked,
                ),
            ],
        )
        return ft.Column(controls=[self.display_view, self.edit_view])

    async def edit_clicked(self, e):
        self.edit_name.value = self.title.value
        self.display_view.visible = False
        self.edit_view.visible = True
        await self.update_async()

    async def save_clicked(self, e):
        self.title.value = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        await self.update_async()

    async def status_changed(self, e):
        self.done = self.done_check.value # type: ignore
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
        self.new_task = ft.TextField(
            label=self.ui_text[0],
            expand=True,
            on_submit=self.add_clicked
        )

        self.deadline_label = ft.Text(
            value="No deadline"
        )

        self.date_button = ft.IconButton(
            icon=ft.icons.CALENDAR_TODAY,
            on_click=lambda _: print("Pressed date")
        )

        self.deadline = ft.Row(
            controls=[
                self.deadline_label,
                self.date_button
            ],
            alignment=ft.MainAxisAlignment.END
        )

        self.tasks = ft.Column()
    
        self.filter = ft.Tabs(
                scrollable=False,
                selected_index=0,
                on_change=self.tabs_changed,
                tabs=[
                    ft.Tab(text=self.ui_text[1]),
                    ft.Tab(text=self.ui_text[2]),
                    ft.Tab(text=self.ui_text[3]),
                    #ft.Tab(text=self.ui_text[4])
                ],
            )
        
        self.items_left = ft.Text(
            value="Items left: 0"
        )
        
        return ft.Column(
            width=600,
            controls=[
                ft.Row(
                    controls=[
                        self.new_task,
                        ft.FloatingActionButton(
                            icon=ft.icons.ADD,
                            on_click=self.add_clicked
                        ),
                    ],
                ),
                self.deadline,
                ft.Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.tasks,
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                self.items_left,
                                ft.OutlinedButton(
                                    text=self.ui_text[5], on_click=self.clear_clicked
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
    
    async def add_clicked(self, e):
        if self.new_task.value:
            if self.deadline_label.value == "-":
                deadline = None
            else:
                deadline = self.deadline_label.value
            task = TaskControl(self.new_task.value, self.task_status_change, self.task_delete) # type: ignore
            self.tasks.controls.append(task) # type: ignore
            self.new_task.value = ""
            self.deadline_label.value = "-"
            await self.new_task.focus_async()
            await self.update_async()

    async def task_status_change(self, task):
        await self.update_async()

    async def task_delete(self, task):
        self.tasks.controls.remove(task)
        await self.update_async()

    async def tabs_changed(self, e):
        await self.update_async()

    async def clear_clicked(self, e):
        for task in self.tasks.controls[:]:
            if task.done: # type: ignore
                await self.task_delete(task)

    async def update_async(self):
        status = self.filter.tabs[self.filter.selected_index].text # type: ignore
        count = 0
        for task in self.tasks.controls:
            task.visible = (
                status == self.ui_text[1]
                or (status == self.ui_text[2] and task.done == False) # type: ignore
                or (status == self.ui_text[3] and task.done) # type: ignore
            )
            if not task.done: # type: ignore
                count += 1
        self.items_left.value = f"{count} active item(s) left"
        await super().update_async()