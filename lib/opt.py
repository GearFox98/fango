import flet as ft
import lib.libfango as libfango

# Main UI

# Counters
work_counter = ft.TextField(
    #value=fang_o_clock['work'],
    multiline=False,
    text_align=ft.TextAlign.RIGHT,
    label="Tiempo de trabajo",
    width=250
)

free_counter = ft.TextField(
    #value=fang_o_clock['free'],
    multiline=False,
    text_align=ft.TextAlign.RIGHT,
    label="Tiempo de descanso",
    width=250
)

lfree_counter = ft.TextField(
    #value=fang_o_clock['long_free'],
    multiline=False,
    text_align=ft.TextAlign.RIGHT,
    label="Tiempo de descanso largo",
    width=250
)

check_button = ft.IconButton(
    icon=ft.icons.CHECK
)

stats = ft.Checkbox(
    label="Guardar estadísticas",
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

save = ft.TextButton(
    text="Guardar",
    icon=ft.icons.SAVE,
    icon_color=ft.colors.BLACK
)
