import os, time, json, logging, asyncio
from enum import Enum
from desktop_notifier import DesktopNotifier

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
CONFIG = "./config.json"
NOTIFIER = DesktopNotifier(app_name="Fango", app_icon="assets/fango.png")

class MODES(Enum):
    WORKING = 0,
    FREE = 1,

# Values for timer
class pomodoro_timer:
    work_time: int = 25
    free_time: int = 5
    long_free_time: int = 15
    loop: int = 1

    def __init__(self, work_time: int = 25, free_time: int = 5, long_free_time: int = 15, loop: int = 1):
        if not os.path.exists(CONFIG): # Generate config file
            self.work_time = work_time
            self.free_time = free_time
            self.long_free_time = long_free_time
            self.loop = loop

            pomodoro = self.get_pomodoro()

            # Dump file
            with open(CONFIG, mode='w') as conf:
                json.dump(pomodoro, fp=conf, indent=4)
            logging.info("Pomodoro config initialized")
        else: # Load file
            with open(CONFIG, mode='r') as conf:
                temp = json.load(conf)
                self.work_time = temp['work']
                self.free_time = temp['free']
                self.long_free_time = temp['long_free']
                self.loop = temp['loop']
            logging.info("Pomodoro config loaded")
    
    def set_loop(self, loop: int):
        self.loop = loop
    
    def add_loop(self):
        self.loop += 1
        if self.loop == 9:
            self.loop = 1

    def get_wtime(self) -> int:
        return self.work_time
    
    def get_ftime(self) -> int:
        return self.free_time
    
    def get_lftime(self) -> int:
        return self.long_free_time
    
    def get_loop(self) -> int:
        return self.loop
    
    def get_pomodoro(self) -> dict:
        pomodoro = {
            'work' : self.work_time,
            'free' : self.free_time,
            'long_free' : self.long_free_time,
            'loop' : self.loop
        }

        return pomodoro

async def notify(message):
    notification = await NOTIFIER.send(title="Fango", message=message, sound=True)

    await asyncio.sleep(5)

    await NOTIFIER.clear(notification)
    await NOTIFIER.clear_all()

# Chrono
async def counting(pomodoro: pomodoro_timer, counting: int = 1) -> int:
    # Reset counter
    if counting == 9:
        counting = 1
    
    if counting % 8 == 0:
        mode = MODES.FREE
        current_timer = pomodoro.get_lftime()
    elif counting % 2 == 0:
        mode = MODES.FREE
        current_timer = pomodoro.get_ftime()
    else:
        mode = MODES.WORKING
        current_timer = pomodoro.get_wtime()

    seconds = current_timer * 60

    if mode == MODES.FREE:
        await notify(f"Comienza descanso de {current_timer} minutos")
    else:
        await notify(f"Comienza el tiempo de trabajo")

    while seconds:
        mins, sec = divmod(seconds, 60)
        timer = '{:02d}:{:02d}'.format(mins, sec)
        print(timer, end='\r')
        time.sleep(1)
        seconds -= 1
    
    if mode == MODES.FREE:
        await notify(f"Terminó el tiempo de descanso de {current_timer} minutos")
    else:
        await notify("Terminó el tiempo de trabajo")

    counting += 1
    return counting

# Main loop
async def main():
    pomodoro = pomodoro_timer()
    
    await counting(pomodoro)
    pomodoro.add_loop()

asyncio.run(main())