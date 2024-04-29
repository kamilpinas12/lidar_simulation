import json

try:
    keyboard_lib = json.load(open("simulation/config.json"))["keyboard_library"]

except:
    keyboard_lib = False

if keyboard_lib:
    from keyboard import is_pressed
else:
    from pynput import keyboard


class Keyboard():
    def __init__(self):
        self.keyboard_lib = keyboard_lib
        if not keyboard_lib:
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()
            self.pressed_key = None


    def on_press(self, key):
        try:
            self.pressed_key = key.char
        except:
            self.pressed_key = None


    def is_key_pressed(self, key):
        if self.keyboard_lib:
            return is_pressed(key)
        else:
            if self.pressed_key == key:
                self.pressed_key = None
                return True
            else:
                return False

