from time import sleep

import pyautogui
import pyperclip
import sqlite3
import utils
import os

def operate_mouse(x, y, time, name, positions):
    pyautogui.moveTo(x, y)
    sleep(1)
    pyautogui.click()
    pyautogui.click()
    sleep(1)
    pyautogui.moveTo(positions[5][0], positions[5][1])
    pyautogui.click()
    # pyautogui.typewrite(name)
    pyperclip.copy(name)
    pyautogui.hotkey('ctrl', 'v')
    sleep(1)
    pyautogui.moveTo(positions[6][0], positions[6][1])
    # sleep(1)
    pyautogui.click()
    pyautogui.moveTo(positions[7][0], positions[7][1])
    sleep(1)
    pyautogui.click()
    pyautogui.typewrite(time)
    pyautogui.moveTo(positions[8][0], positions[8][1])
    sleep(1)
    pyautogui.click()
    pyautogui.typewrite(time)
    pyautogui.moveTo(positions[9][0], positions[9][1])
    sleep(1)
    pyautogui.click()


def auto_calendar(name, time, webname, positions):
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    database_path = os.path.join(data_dir, f'{webname}_contests.db')
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute(''' create table if not exists contests(
        time text,
        name text
    )''')
    cursor.execute("select * from contests where name = ?", (name,))
    result = cursor.fetchone()
    if not result:
        utils.auto_calendar0(time, name, webname, positions)
        cursor.execute("insert into contests values(?, ?)", (time, name))
        conn.commit()
    cursor.close()
    conn.close()
