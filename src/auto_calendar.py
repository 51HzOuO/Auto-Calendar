from datetime import datetime
from bs4 import BeautifulSoup
from urllib import parse
from time import sleep

import requests.utils
import webbrowser
import operatorr
import requests
import json
import os
import re


class auto_calendar:
    positions = []

    def __init__(self):
        url = "https://outlook.live.com/calendar/0/view/month"
        webbrowser.open(url, autoraise=True)

        dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(dir, '..', 'data')
        os.makedirs(dir, exist_ok=True)
        file_path = os.path.join(data_dir, 'position.txt')

        with open(file_path, 'r') as file:
            for line in file:
                x, y = line.strip().split(',')
                self.positions.append((int(x), int(y)))

        sleep(3)

    def get_codeforces_contest(self):
        url = "https://codeforces.com/contests"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find_all('table')[0]
        rows = table.find_all('tr')
        contests = []
        for row in rows[1:]:
            cols = row.find_all('td')
            time = cols[2].get_text()
            name = cols[0].get_text()
            operatorr.auto_calendar(name, time, 'codeforces', self.positions)

    def get_nowcoder_contest(self):
        url = "https://ac.nowcoder.com/acm/contest/vip-index"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        contests = soup.find_all('div', class_="platform-item-main")
        for contest in contests:
            name = contest.find('a', href=True).text
            time = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}',
                             contest.find('li', class_="match-time-icon").text.strip()).group(0)
            if time > datetime.now().strftime("%Y-%m-%d %H:%M"):
                operatorr.auto_calendar(name, time, 'nowcoder', self.positions)

    def get_atcoder_contest(self):
        url = "https://atcoder.jp/contests/"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        contests = soup.find('div', id="contest-table-upcoming").find('tbody').find_all('tr')
        for contest in contests:
            name = contest.find_all('td')[1].find('a', href=True).text
            time = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}',
                             contest.find('time', class_="fixtime-full").text.strip()).group(0)
            operatorr.auto_calendar(name, time, 'atcoder', self.positions)

    def get_luogu_contest(self):
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
        decoded_json_string = parse.unquote(encoded_json_string).encode('utf-8').decode('unicode_escape').replace('\\/',
                                                                                                                  '/')
        contests = json.loads(decoded_json_string).get('currentData').get('contests').get('result')
        for contest in contests:
            time = contest['startTime']
            if time > datetime.now().timestamp():
                name = contest['name']
                time = datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M")
                operatorr.auto_calendar(name, time, 'luogu', self.positions)
