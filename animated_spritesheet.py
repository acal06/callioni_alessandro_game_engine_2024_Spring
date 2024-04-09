import pygame as pg

FPS = 30

frames = ["Frame 1", "Frame 2", "Frame 3", "Frame 4"]

clock = pg.time.Clock()

current_frame = 0
last_update = 0

def animate():
    global last_update
    global current_frame
    now = pg.time.get_ticks()
    if now - last_update > 350:
        current_frame = (current_frame + 1) % len(frames)
        print(frames[current_frame])
        # last_update = now
    # print(now)

while True:
    clock.tick(FPS)
    animate()
    