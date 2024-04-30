import flet as ft
import asyncio, os, time, asyncio
import lib.libfango as libfango

from desktop_notifier import DesktopNotifier

data = {
    'clock' : '00:00',
    'mode' : 0,
    'run' : False
}

run = False

NOTIFIER = DesktopNotifier(app_name="Fango", app_icon="assets/fango.png")

# Notifier
async def notify(message):
    notification = await NOTIFIER.send(title="Fango",
                                 message=message,
                                 sound=True)

    time.sleep(5)

    await NOTIFIER.clear(notification)
    await NOTIFIER.clear_all()

# Main UI
async def main(page: ft.Page):
    page.title = "Fango"
    page.padding = 0
    page.window_maximizable = False
    page.window_width = 415
    page.window_height = 415
    page.window_resizable = False

    clock = ft.Text(value='00:00', text_align=ft.TextAlign.CENTER, size=46)
    timer = ft.Container(clock,
                         width=410,
                         height=330,
                         alignment=ft.alignment.center)

    # Threaded Functions
    def pomodoro_timer(_e):
        pomodoro = libfango.pomodoro_timer()
        loop = pomodoro.get_loop()

        data = libfango.get_data(pomodoro, loop)

        seconds = data['current_timer'] * 60

        while seconds:
            mins, sec = divmod(seconds, 60)
            timer = '{:02d}:{:02d}'.format(mins, sec)
            print(timer, end='\r')
            clock.value = timer
            page.update()
            time.sleep(1)
            seconds -= 1
    
        pomodoro.add_loop()

        if data['mode'] == libfango.MODES.FREE:
            # "Terminó el tiempo de descanso de {current_timer} minutos"
            asyncio.run(notify(f"Terminó el tiempo de {data['current_timer']} minutos"))
        else:
            # "Terminó el tiempo de trabajo"
            asyncio.run(notify("Terminó el tiempo de trabajo"))

    # UI
    page.appbar = ft.AppBar(
        title=ft.Text("Fango"),
        actions=[
            ft.TextButton(text="Iniciar",
                          icon=ft.icons.PLAY_ARROW,
                          icon_color=ft.colors.BLACK,
                          on_click=pomodoro_timer),
            ft.TextButton(content=ft.Row([
                ft.Icon(name=ft.icons.SETTINGS,
                        color=ft.colors.BLACK)
                        ]),
                width=50)
        ]
    )

    await page.add_async(timer)

if not os.path.exists(os.path.expanduser("~/.fango")):
    os.mkdir(os.path.expanduser("~/.fango"))

ft.app(target=main)