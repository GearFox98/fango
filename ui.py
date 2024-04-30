import flet as ft
import asyncio, os, time, asyncio, threading, concurrent.futures
import lib.libfango as libfango

from desktop_notifier import DesktopNotifier, Button

data = {
    'clock' : '00:00',
    'mode' : 0
}

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
    page.window_max_height = 415
    page.window_max_width = 415
    page.window_min_height = 415
    page.window_min_width = 415
    page.window_maximizable = False

    clock = ft.Text(value='00:00', text_align=ft.TextAlign.CENTER, size=46)

    # Threaded Functions
    def pomodoro_timer():
        pomodoro = libfango.pomodoro_timer()
        loop = pomodoro.get_loop()

        x = libfango.counting(pomodoro, data, 2)
        return x
    
    def update_clock():
        while True:
            clock.value = data["clock"]
            page.update()
            if data["clock"] == '00:00':
                break

    def start_timer_thread(arg):
        t = threading.Thread(target=pomodoro_timer, daemon=True)
        u = threading.Thread(target=update_clock, daemon=True)
        
        t.start()
        u.start()
        
    def test(a):
        clock.value = data["clock"]
        page.update()

    # UI
    page.appbar = ft.AppBar(
        title=ft.Text("Fango"),
        actions=[
            ft.TextButton(text="Iniciar",
                          icon=ft.icons.PLAY_ARROW,
                          icon_color=ft.colors.BLACK,
                          on_click=start_timer_thread),
            ft.TextButton(content=ft.Row([
                ft.Icon(name=ft.icons.SETTINGS,
                        color=ft.colors.BLACK)
                        ]),
                width=50,
                on_click=test)
        ]
    )

    TIMER = ft.Container(clock,
                         width=410,
                         height=330,
                         alignment=ft.alignment.center)

    await page.add_async(TIMER)

if not os.path.exists(os.path.expanduser("~/.fango")):
    os.mkdir(os.path.expanduser("~/.fango"))

asyncio.run(ft.app_async(target=main))