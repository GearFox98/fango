import flet as ft
import lib.libfango as libfango

# Main UI

# Counters
work_counter = ft.TextField(
    multiline=False,
    text_align=ft.TextAlign.RIGHT,
    label="Tiempo de trabajo",
    width=250
)

free_counter = ft.TextField(
    multiline=False,
    text_align=ft.TextAlign.RIGHT,
    label="Tiempo de descanso",
    width=250
)

lfree_counter = ft.TextField(
    multiline=False,
    text_align=ft.TextAlign.RIGHT,
    label="Tiempo de descanso largo",
    width=250
)

check_button = ft.IconButton(
    icon=ft.icons.CHECK
)

stats = ft.Checkbox(
    label="Guardar estadísticas de tiempo",
    value=False
)

lang = ft.Dropdown(
    value="ES",
    options=[
        ft.dropdown.Option(
            key='ES',
            text='Español'
        ),
        ft.dropdown.Option(
            key='EN',
            text='English'
        )
    ],
    icon=ft.icons.LANGUAGE,
    width=170
)

theme = ft.Dropdown(
    value="SYSTEM",
    options=[
        ft.dropdown.Option(
            key="LIGHT",
            text='Claro'
        ),
        ft.dropdown.Option(
            key="DARK",
            text='Oscuro'
        )
    ],
    icon=ft.icons.PALETTE,
    width=170
)

theme_switch = ft.IconButton(
    icon=ft.icons.SUNNY
)

save = ft.TextButton(
    text="Guardar todo",
    icon=ft.icons.SAVE
)
