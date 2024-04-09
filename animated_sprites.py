import time


frames = ["Frame 1, Frame 2, Frame 3, Frame 4"]


while True:
    time.sleep(1)
    print(str(frames))

z = 1
while True:
    time.sleep(1)
    print("Frame " + str(z))
    z += 1
    