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

# Form components
work = ft.Container(
    ft.Row(
        [
            work_counter,
            ft.IconButton(
                icon=ft.icons.CHECK,
                #on_click=lambda _: libfango.set_option(page=page, work=work_counter, field_type="work")
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY
    ),
    padding=ft.padding.only(0,10,0,0)
)

free = ft.Container(
    ft.Row(
        [
            free_counter,
            ft.IconButton(
                icon=ft.icons.CHECK,
                #on_click=lambda _: libfango.set_option(page=page, work=free_counter, field_type="free")
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY
    ),
    padding=ft.padding.only(0,10,0,0)
)

long_free = ft.Container(
    ft.Row(
        [
            lfree_counter,
            ft.IconButton(
                icon=ft.icons.CHECK,
                #on_click=lambda _: libfango.set_option(page=page, work=lfree_counter, field_type="lfree")
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY
    ),
    padding=ft.padding.only(0,10,0,20),
    alignment=ft.alignment.center
)

stats = ft.Checkbox(
    label="Guardar estadísticas",
    #value=
)

lang = ft.Dropdown(
    #value,
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

misc = ft.Row(
    [
        stats,
        lang
    ],
    alignment=ft.MainAxisAlignment.SPACE_AROUND
)

# Options component
form = ft.Container(
    ft.Column(
        [
            work,
            free,
            long_free,
            misc
        ]
    ),
    padding=ft.padding.only(10,10,10,20)
)

# UI
save = ft.TextButton(
    text="Guardar",
    icon=ft.icons.SAVE,
    icon_color=ft.colors.BLACK,
    #on_click=save
)

back = ft.TextButton(
    content=ft.Row(
        [
            ft.Icon(
                name=ft.icons.ARROW_BACK,
                color=ft.colors.BLACK
            )
        ]
    ),
    width=50,
    #on_click=back_to_timer
)

# App menu
appbar = ft.AppBar(
    title=ft.Text("Configuracion", weight=ft.FontWeight.BOLD),
    actions=[
        back,
        save
    ]
)
