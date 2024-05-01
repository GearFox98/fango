from concurrent.futures import thread
from pdb import run
import threading
import flet as ft
import asyncio, os, time, asyncio
import lib.libfango as libfango

from desktop_notifier import DesktopNotifier

data = {
    'clock' : '00:00',
    'mode' : 0,
    'run' : False
}

NOTIFIER = DesktopNotifier(app_name="Fango", app_icon="assets/fango.png")

# Notifier
async def notify(message):
    notification = await NOTIFIER.send(
        title="Fango",
        message=message,
        sound=True
    )

    time.sleep(5)

    await NOTIFIER.clear(notification)
    await NOTIFIER.clear_all()

# Main UI
async def main(page: ft.Page):
    page.title = "Fango"
    page.window_max_height = 415
    page.window_max_width = 415
    page.window_min_height = 415
    page.window_min_width = 415
    #page.window_width = 415
    #page.window_height = 415
    #page.window_resizable = False
    page.window_maximizable = False
    page.padding = 0

    clock = ft.Text(value='00:00', text_align=ft.TextAlign.CENTER, size=46)
    timer = ft.Container(
        clock,
        width=410,
        height=330,
        alignment=ft.alignment.center
    )

    # Threaded Functions
    breaker = threading.Event()

    def pomodoro_timer():
        pomodoro = libfango.pomodoro_timer()
        loop = pomodoro.get_loop()

        data = libfango.get_data(pomodoro, loop)

        seconds = data['current_timer'] * 60
        try:
            while seconds:
                if breaker.is_set():
                    raise Exception("Requested halt")
                mins, sec = divmod(seconds, 60)
                timer = '{:02d}:{:02d}'.format(mins, sec)
                print(timer, end='\r')
                clock.value = timer
                page.update()
                time.sleep(1)
                seconds -= 1
        
            pomodoro.add_loop()

            if data['mode'] == libfango.MODES.FREE:
                asyncio.run(notify(f"Terminó el tiempo de {data['current_timer']} minutos"))
            else:
                asyncio.run(notify("Terminó el tiempo de trabajo"))
        except Exception as e:
            print("Timer stopped")
        finally:
            clock.value = "00:00"
            page.update()

    def set_breaker(_e):
        if data['run'] == False:
            breaker.clear()
            data['run'] = True
            main_button.icon = ft.icons.STOP
            main_button.text = "Detener"
            t = threading.Thread(target=pomodoro_timer, daemon=True)
            t.start()
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

    option_button = ft.TextButton(
        content=ft.Row(
            [
                ft.Icon(
                    name=ft.icons.SETTINGS,
                    color=ft.colors.BLACK
                )
            ]
        ),
        width=50
    )

    page.appbar = ft.AppBar(
        title=ft.Text("Fango"),
        actions=[
            main_button,
            option_button
        ]
    )

    await page.add_async(timer)

if not os.path.exists(os.path.expanduser("~/.fango")):
    os.mkdir(os.path.expanduser("~/.fango"))

ft.app(target=main)
