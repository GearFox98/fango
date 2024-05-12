import threading
import flet as ft
import os, time
import lib.libfango as libfango
import lib.opt as opt

from math import pi

data = {
    'clock' : '00:00',
    'mode' : 0,
    'run' : False
}

# Main UI
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

    # Timer
    pomodoro = libfango.pomodoro_timer()
    pomodoro_data = pomodoro.get_pomodoro()
    # Configuration
    config_data = libfango.config_file().get_conf()

    # MAIN PAGE
    clock = ft.Text(value='00:00', text_align=ft.TextAlign.CENTER, size=54)
    progress = ft.ProgressRing(value=0.5, rotate=-pi/2, width=300, height=300, stroke_width=30, color=ft.colors.BLUE)
    progress_shadow = ft.ProgressRing(value=0.5, rotate=-pi/2, width=300, height=300, stroke_width=30, color=ft.colors.GREY)
    
    # Stages attributes
    loop_label = ft.Text("Sesión: 0", size=24)
    mode_label = ft.Text("Trabajo", size=24)
    
    # Stages (Below the clock)
    stages = ft.Row(
        [
            loop_label, # Loop Number
            mode_label # Mode
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # Timer component
    timer = ft.Container(
        ft.Stack(
            [
                ft.Container(
                    content=progress_shadow,
                    width=410,
                    height=330,
                    alignment=ft.alignment.center
                ),
                ft.Container(
                    content=progress,
                    width=410,
                    height=330,
                    alignment=ft.alignment.center
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(height=30),
                            ft.Row([clock], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Divider(),
                            stages,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        
                    ),
                    width=410,
                    height=330,
                    alignment=ft.alignment.center,
                    padding=35
                )
            ]
        )
    )

    # Animate progress
    def anim_progress(start: int, end: int, step: int):
        for i in range(start, end, step):
            progress.value = (i / 100)/2
            time.sleep(0.005)
            page.update()

    # Threaded Functions
    # moved to lib/libfango.py
    # To cancel the process
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
                args=[page, clock, progress, mode_label, loop_label, breaker],
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

    # UI
    main_button = ft.TextButton(
        text="Iniciar",
        icon=ft.icons.PLAY_ARROW,
        icon_color=ft.colors.BLACK,
        on_click=set_breaker
    )

    def opt_btn_func(_e):
        pomodoro_data = libfango.pomodoro_timer().get_pomodoro()
        page.go("/conf")

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
        on_click=opt_btn_func
    )

    # App menu
    main_appbar = ft.AppBar(
        title=ft.Text(libfango.APP_NAME, weight=ft.FontWeight.BOLD),
        actions=[
            main_button,
            option_button
        ],
        #bgcolor=ft.colors.SURFACE_VARIANT
    )

    # CONFIG
    # Counters
    work_counter = opt.work_counter
    free_counter = opt.free_counter
    lfree_counter = opt.lfree_counter

    work_counter.value = pomodoro_data['work']
    free_counter.value = pomodoro_data['free']
    lfree_counter.value = pomodoro_data['long_free']

    # Form components
    work = ft.Container(
        ft.Row(
            [
                work_counter,
                ft.IconButton(
                    icon=ft.icons.CHECK,
                    on_click=lambda _: libfango.set_option(pomodoro=pomodoro, page=page, text_field=work_counter, field_type="work") # type: ignore
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
                    on_click=lambda _: libfango.set_option(pomodoro=pomodoro, page=page, text_field=free_counter, field_type="free") # type: ignore
                )
            ], # type: ignore
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
                    on_click=lambda _: libfango.set_option(pomodoro=pomodoro, page=page, text_field=lfree_counter, field_type="lfree") # type: ignore
                )
            ], # type: ignore
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        ),
        padding=ft.padding.only(0,10,0,20),
        alignment=ft.alignment.center
    )

    # Other opts
    stats = opt.stats
    lang = opt.lang

    stats.value = config_data['stats']
    lang.value = config_data['lang']

    misc = ft.Row(
        [
            stats,
            lang
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND
    )

    # Integrate everything
    config_form = ft.Container(
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

    # Appbar items
    save_button = opt.save

    save_button.on_click = lambda _: libfango.save_all(pomodoro, page, work_counter, free_counter, lfree_counter, stats, lang, libfango.THEME['SYSTEM'])

    opt_appbar = ft.AppBar(
        title=ft.Text("Configuracion", weight=ft.FontWeight.BOLD),
        actions=[
            save_button
        ]
    )

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    main_appbar,
                    timer
                ],
            )
        )
        if page.route == "/conf":
            page.views.append(
                ft.View(
                    "/conf",
                    [
                        opt_appbar,
                        config_form
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

    page.add(timer)

# Create config folder
if not os.path.exists(os.path.expanduser("~/.fango")):
    os.mkdir(os.path.expanduser("~/.fango"))

ft.app(target=main)
