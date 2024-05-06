from datetime import datetime, timedelta
from datetime import date
from PIL import ImageGrab

import pyautogui
import pytesseract
import operatorr
import re

def auto_calendar0(time, name, webname, positions):
    img_which_week = ImageGrab.grab(bbox=(positions[0][0], positions[0][1], positions[1][0], positions[1][1]))
    img_which_day = ImageGrab.grab(bbox=(positions[0][0], positions[0][1], positions[2][0], positions[2][1]))
    custom_config = r'--oem 3 --psm 6'

    text_data_week = pytesseract.image_to_data(img_which_week, output_type=pytesseract.Output.DATAFRAME,
                                               lang='chi_sim+eng', config=custom_config)
    text_data_day = pytesseract.image_to_data(img_which_day, output_type=pytesseract.Output.DATAFRAME,
                                              lang='chi_sim+eng', config=custom_config)

    pattern = r'\b([1-9]|[1-4][0-9]|5[0-3])\b'
    filtered_text = text_data_week[text_data_week['text'].astype(str).apply(lambda x: bool(re.search(pattern, x)))]
    filtered_text = filtered_text[['left', 'top', 'height', 'text']]
    week = filtered_text.to_dict(orient='records')

    year, m, d, time_str = parse_time(time, webname)
    maxn, minn = 0, 100

    for i in week:
        maxn = max(maxn, int(i['text']))
        minn = min(minn, int(i['text']))
    count = 0
    while maxn < get_week_of_year(m, d, year) and count < 5:
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
            maxn = max(maxn, int(i['text']))
            minn = min(minn, int(i['text']))

    count = 0
    while minn > get_week_of_year(m, d, year) and count < 5:
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
            maxn = max(maxn, int(i['text']))
            minn = min(minn, int(i['text']))

    pattern = r'[一二三四五六日]'
    filtered_day = text_data_day[text_data_day['text'].astype(str).apply(lambda x: bool(re.search(pattern, x)))]
    filtered_day = filtered_day[['left', 'top', 'height', 'text']]
    day = filtered_day.to_dict(orient='records')

    the_week = get_week_of_year(m, d, year)
    the_day = get_day_of_week(m, d, year)

    for y in week:
        if int(y['text']) == the_week:
            for x in day:
                if x['text'] == the_day:
                    operatorr.operate_mouse(int(x['left']) + positions[0][0], int(y['top']) + positions[0][1], time_str, name, positions)


# def auto_calendar(name, time, webname):
#     data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
#     os.makedirs(data_dir, exist_ok=True)
#     database_path = os.path.join(data_dir, f'{webname}_contests.db')
#     conn = sqlite3.connect(database_path)
#     cursor = conn.cursor()
#     cursor.execute(''' create table if not exists contests(
#         time text,
#         name text
#     )''')
#     cursor.execute("select * from contests where name = ?", (name,))
#     result = cursor.fetchone()
#     if not result:
#         auto_calendar0(time, name, webname)
#         cursor.execute("insert into contests values(?, ?)", (time, name))
#         conn.commit()
#     cursor.close()
#     conn.close()

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
