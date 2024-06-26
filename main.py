import tkinter as tk
from pynput import mouse, keyboard
from threading import Thread
import time

mouse_controller = mouse.Controller()
keyboard_controller = keyboard.Controller()

root = tk.Tk()
root.title('Clicker')
root.geometry('200x450')
root.resizable(width=False, height=False)

hotkey_var = tk.StringVar()

click_interval = 1
selected_button = None
running = False
hotkey_value = None


def callback(value):
    global selected_button
    selected_button = value
    print("Selected button:", selected_button)


def auto_clicker():
    global running
    while running:
        if selected_button:
            if selected_button == 'LMB':
                mouse_controller.click(mouse.Button.left)
            elif selected_button == 'RMB':
                mouse_controller.click(mouse.Button.right)
            elif selected_button == 'MOUSE 3':
                mouse_controller.click(mouse.Button.middle)
            elif selected_button.startswith('MOUSE'):
                button_number = int(selected_button.split()[-1])
                mouse_controller.click(mouse.Button(button_number))
            elif selected_button == 'SPACE':
                keyboard_controller.press(' ')
                keyboard_controller.release(' ')
            elif selected_button == 'ENTER':
                keyboard_controller.press(keyboard.Key.enter)
                keyboard_controller.release(keyboard.Key.enter)
            else:
                keyboard_controller.press(selected_button.lower())
                keyboard_controller.release(selected_button.lower())
        time.sleep(click_interval)


def start_clicking():
    global running
    if not running:
        running = True
        Thread(target=auto_clicker).start()


def stop_clicking():
    global running
    running = False


def toggle_clicking(key):
    global running, hotkey_value
    if hasattr(key, 'char') and key.char == hotkey_value or hasattr(key, 'vk') and key.vk == hotkey_value:
        if running:
            stop_clicking()
        else:
            start_clicking()


def start_listening():
    global listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()


def on_press(key):
    global hotkey_value, listener
    try:
        hotkey_value = key.char
    except AttributeError:
        if key == keyboard.Key.space:
            hotkey_value = ' '
        elif key == keyboard.Key.enter:
            hotkey_value = keyboard.Key.enter
        else:
            hotkey_value = key.vk
    hotkey_picked.config(text=f"Hotkey set to: {hotkey_value}")
    hotkey_var.set(str(hotkey_value))
    listener.stop()


def show():
    time_s = tk.Entry(width=10)
    time_s.pack(pady=(5, 0))
    return time_s


def pick(f):
    timepick = tk.Label(root, text=f, font='Times 10')
    timepick.pack(pady=(5, 0))
    entry = show()
    return entry


def update_click_interval():
    global click_interval
    try:
        hours = int(hours_entry.get() or 0)
        minutes = int(minutes_entry.get() or 0)
        seconds = int(seconds_entry.get() or 0)
        milliseconds = int(milliseconds_entry.get() or 0)
        click_interval = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
    except ValueError:
        click_interval = 1


def global_listener():
    with keyboard.Listener(on_press=toggle_clicking) as listener:
        listener.join()


time_label = tk.Label(root, anchor='nw', text='Click interval:', font=5)
time_label.pack()

time_prom = ['Hours:', "Minutes:", "Seconds:", 'Milliseconds:']
entries = []
for i in time_prom:
    entry = pick(i)
    entries.append(entry)

hours_entry, minutes_entry, seconds_entry, milliseconds_entry = entries

update_button = tk.Button(root, text="Update Interval", command=update_click_interval)
update_button.pack(pady=(5, 0))

button_pick = tk.Label(root, text='Button:', font=10)
button_pick.pack(pady=(5, 0))

options = ['LMB', 'RMB', 'SPACE', 'ENTER', 'MOUSE 3', 'MOUSE 4', 'MOUSE 5', 'W', 'A', 'S', 'D']
variable = tk.StringVar(root)
variable.trace("w", lambda name, index, mode: callback(variable.get()))
option_menu = tk.OptionMenu(root, variable, *options)
option_menu.pack()

hotkey_pick = tk.Button(root, text="Set hotkey", command=start_listening)
hotkey_pick.pack(pady=(10, 5))

hotkey_picked = tk.Label(root, textvariable=hotkey_var)
hotkey_picked.pack()

global_listener_thread = Thread(target=global_listener)
global_listener_thread.daemon = True
global_listener_thread.start()

root.mainloop()
