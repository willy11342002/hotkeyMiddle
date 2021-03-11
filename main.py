import pyautogui
import keyboard
import pynput

# keyboard.add_hotkey('ctrl+alt', pyautogui.middleClick)
# keyboard.wait()


alt = False
ctrl = False
alt_list = [
    pynput.keyboard.Key.alt_l,
    pynput.keyboard.Key.alt_gr,
]
ctrl_list = [
    pynput.keyboard.Key.ctrl_l,
    pynput.keyboard.Key.ctrl_r,
]

def on_press(key):
    global alt, ctrl
    
    if key in alt_list:
        alt = True
    if key in ctrl_list:
        ctrl = True

    if alt and ctrl:
        pyautogui.middleClick()
        alt = ctrl = False

def on_release(key):
    global alt, ctrl
    if key in alt_list:
        alt = False
    if key in ctrl_list:
        ctrl = False

with pynput.keyboard.Listener(
    on_press=on_press,
    on_release=on_release
) as listener:
    listener.join()
