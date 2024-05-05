from PIL import ImageGrab
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from datetime import date
from urllib import parse
import os
import pyautogui
import pyperclip
import sqlite3
import requests
import webbrowser
import pytesseract
import re
import json
import requests.utils

def get_week_of_year(m, d, y):
    return date(y, m, d).isocalendar()[1]

def get_day_of_week(m, d, y):
    days_chinese = ["一", "二", "三", "四", "五", "六", "日"]
    return days_chinese[date(y, m, d).weekday()]

def parse_time(time, webname):
    clean_time = time.strip()

    if webname == 'nowcoder':
        date_obj = datetime.strptime(clean_time, "%Y-%m-%d %H:%M")
    elif webname == 'codeforces':
        date_obj = datetime.strptime(clean_time, "%b/%d/%Y %H:%M")
        date_obj += timedelta(hours=5)
    elif webname == 'atcoder':
        date_obj = datetime.strptime(clean_time, "%Y-%m-%d %H:%M")
        date_obj -= timedelta(hours=1)
    elif webname == 'luogu':
        date_obj = datetime.strptime(clean_time, "%Y-%m-%d %H:%M")

    time_str = date_obj.strftime("%H:%M")
    return date_obj.year, date_obj.month, date_obj.day, time_str

def operate_mouse(x, y, time, name):
    pyautogui.moveTo(x, y)
    # sleep(1)
    pyautogui.click()
    pyautogui.click()
    sleep(1)
    pyautogui.moveTo(positions[5][0], positions[5][1])
    pyautogui.click()
    # pyautogui.typewrite(name)
    pyperclip.copy(name)
    pyautogui.hotkey('ctrl', 'v')
    # sleep(1)
    pyautogui.moveTo(positions[6][0], positions[6][1])
    # sleep(1)
    pyautogui.click()
    pyautogui.moveTo(positions[7][0], positions[7][1])
    # sleep(1)
    pyautogui.click()
    pyautogui.typewrite(time)
    pyautogui.moveTo(positions[8][0], positions[8][1])
    # sleep(1)
    pyautogui.click()
    pyautogui.typewrite(time)
    pyautogui.moveTo(positions[9][0], positions[9][1])
    # sleep(1)
    pyautogui.click()

def auto_calendar(time, name, webname):
    img_which_week = ImageGrab.grab(bbox=(positions[0][0], positions[0][1], positions[1][0], positions[1][1]))
    img_which_day = ImageGrab.grab(bbox=(positions[0][0], positions[0][1], positions[2][0], positions[2][1]))
    custom_config = r'--oem 3 --psm 6'

    text_data_week = pytesseract.image_to_data(img_which_week, output_type=pytesseract.Output.DATAFRAME, lang='chi_sim+eng', config=custom_config)
    text_data_day = pytesseract.image_to_data(img_which_day, output_type=pytesseract.Output.DATAFRAME, lang='chi_sim+eng', config=custom_config)

    pattern = r'\b([1-9]|[1-4][0-9]|5[0-3])\b'
    filtered_text = text_data_week[text_data_week['text'].astype(str).apply(lambda x: bool(re.search(pattern, x)))]
    filtered_text = filtered_text[['left', 'top', 'height', 'text']]
    week = filtered_text.to_dict(orient='records')

    year, m, d, time_str = parse_time(time, webname)
    maxn, minn = 0, 100
    the_week = get_week_of_year(m, d, year)
    the_day = get_day_of_week(m, d, year)

    for i in week:
        maxn = max(maxn, int (i['text']))
        minn = min(minn, int (i['text']))

    count = 0
    while maxn < the_week and count < 5:
        count += 1
        pyautogui.moveTo(positions[4][0], positions[4][1])
        pyautogui.click()
        img_which_week = ImageGrab.grab(bbox=(positions[0][0], positions[0][1], positions[1][0], positions[1][1]))
        custom_config = r'--oem 3 --psm 6'

        text_data_week = pytesseract.image_to_data(img_which_week, output_type=pytesseract.Output.DATAFRAME, lang='chi_sim+eng', config=custom_config)

        pattern = r'\b([1-9]|[1-4][0-9]|5[0-3])\b'
        filtered_text = text_data_week[text_data_week['text'].astype(str).apply(lambda x: bool(re.search(pattern, x)))]
        filtered_text = filtered_text[['left', 'top', 'height', 'text']]
        week = filtered_text.to_dict(orient='records')
        for i in week:
            maxn = max(maxn, int (i['text']))
            minn = min(minn, int (i['text']))

    count = 0
    while minn > the_week and count < 5:
        count += 1
        pyautogui.moveTo(positions[3][0], positions[3][1])
        pyautogui.click()
        img_which_week = ImageGrab.grab(bbox=(positions[0][0], positions[0][1], positions[1][0], positions[1][1]))
        custom_config = r'--oem 3 --psm 6'

        text_data_week = pytesseract.image_to_data(img_which_week, output_type=pytesseract.Output.DATAFRAME, lang='chi_sim+eng', config=custom_config)

        pattern = r'\b([1-9]|[1-4][0-9]|5[0-3])\b'
        filtered_text = text_data_week[text_data_week['text'].astype(str).apply(lambda x: bool(re.search(pattern, x)))]
        filtered_text = filtered_text[['left', 'top', 'height', 'text']]
        week = filtered_text.to_dict(orient='records')
        for i in week:
            maxn = max(maxn, int (i['text']))
            minn = min(minn, int (i['text']))

    pattern = r'[一二三四五六日]'
    filtered_day = text_data_day[text_data_day['text'].astype(str).apply(lambda x: bool(re.search(pattern, x)))]
    filtered_day = filtered_day[['left', 'top', 'height', 'text']]
    day = filtered_day.to_dict(orient='records')

    for y in week:
        if int (y['text']) == the_week:
            for x in day:
                if x['text'] == the_day:
                    operate_mouse(int (x['left']) + positions[0][0], int (y['top']) + positions[0][1], time_str, name)

def check_contest_exist(name, time, webname):
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
        auto_calendar(time, name, webname)
        cursor.execute("insert into contests values(?, ?)", (time, name))
        conn.commit()
    cursor.close()
    conn.close()

def get_codeforces_contest():
    url = "https://codeforces.com/contests?complete=true"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all('table')[0]
    rows = table.find_all('tr')
    contests = []
    for row in rows[1:]:
        cols = row.find_all('td')
        time = cols[2].get_text()
        name = cols[0].get_text()
        check_contest_exist(name, time, 'codeforces')

def get_nowcoder_contest():
    url = "https://ac.nowcoder.com/acm/contest/vip-index"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    contests = soup.find_all('div', class_= "platform-item-main")
    for contest in contests:
        name = contest.find('a', href=True).text
        time = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', contest.find('li', class_= "match-time-icon").text.strip()).group(0)
        check_contest_exist(name, time, 'nowcoder')

def get_atcoder_contest():
    url = "https://atcoder.jp/contests/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    contests = soup.find('div', id="contest-table-upcoming").find('tbody').find_all('tr')
    for contest in contests:
        name = contest.find_all('td')[1].find('a', href=True).text
        time = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', contest.find('time', class_= "fixtime-full").text.strip()).group(0)
        if time > datetime.now().strftime("%Y-%m-%d %H:%M"):
            check_contest_exist(name, time, 'atcoder')

def get_luogu_contest():
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
    }
    url = "https://www.luogu.com.cn/contest/list"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    script_content = soup.find('script').string

    start_index = script_content.find('decodeURIComponent("') + len('decodeURIComponent("')
    end_index = script_content.find('")')

    encoded_json_string = script_content[start_index:end_index]

    decoded_json_string = parse.unquote(encoded_json_string).replace(r'\/', '/').encode('utf-8').decode('unicode_escape')

    contests = json.loads(decoded_json_string).get('currentData').get('contests').get('result')
    for contest in contests:
        time = contest['startTime']
        if time > datetime.now().timestamp():
            name = contest['name']
            time = datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M")
            check_contest_exist(name, time, 'luogu')

# def get_lanqiao_contest():
    # url = "https://www.lanqiao.cn/oj-contest/"
    # page = requests.getd(url)
    # soup = BeautifulSoup(page.content, 'html.parser')
    # with open('lanqiao.html', 'w', encoding='utf-8') as f:
        # f.write(str(soup))
    # print(soup)22:35

positions = []

if __name__ == "__main__":
    url = "https://outlook.live.com/calendar/0/view/month"
    webbrowser.open(url, autoraise = True)
    
    dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(dir, '..', 'data')
    os.makedirs(dir, exist_ok=True)
    file_path = os.path.join(data_dir, 'position.txt')

    with open(file_path, 'r') as file:
        for line in file:
            x, y = line.strip().split(',')
            positions.append((int(x), int(y)))

    sleep(3)
    
    get_nowcoder_contest()
    get_codeforces_contest()
    get_atcoder_contest()
    get_luogu_contest()
    # get_lanqiao_contest()