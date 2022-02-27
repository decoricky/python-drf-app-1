import datetime
import urllib.parse
from typing import List

import requests
from bs4 import BeautifulSoup

JST = datetime.timezone(datetime.timedelta(hours=9))
BASE_URL = "https://www.b-monster.jp"
PAGE_PATH = "reserve/"
URL = urllib.parse.urljoin(BASE_URL, PAGE_PATH)


class ScrapingItem:
    def __init__(self, studio_name, start_time, performer_name, program_name):
        self.studio_name = studio_name
        self.start_time = start_time
        self.performer_name = performer_name
        self.program_name = program_name


def get_schedule_by_studio(
        studio_code: str, studio_name: str, now: datetime.datetime = datetime.datetime.now(JST)) -> List[ScrapingItem]:

    result_list: List[ScrapingItem] = []

    # 日付が変わるタイミングは避ける（23:59~00:01）
    if datetime.time(hour=23, minute=59) <= now.time() or now.time() < datetime.time(hour=0, minute=1):
        return result_list

    # HTML取得
    r = requests.get(URL, params={"studio_code": studio_code})
    try:
        r.raise_for_status()
    except Exception as e:
        raise e

    # HTML解析
    soup = BeautifulSoup(r.text, features="html.parser")
    week = soup.select("body div#scroll-box div.grid div.flex-no-wrap")
    date = now
    for day in week:
        panels = day.select("li.panel")
        for panel in panels:
            time = panel.select("p.tt-time")
            performer = panel.select("p.tt-instructor")
            program = panel.select("p.tt-mode")

            if time and performer and program:
                # プログラム開始時間（HH:MM）
                hour = int(time[0].text[:2])
                minute = int(time[0].text[3:5])
                # パフォーマー
                performer = performer[0].text
                # プログラム名（リミテッド表記を削除）
                program = program[0]["data-program"]
                program = program if "(l)" not in program else program[:-3]
                # パフォーマー名またはプログラム名が未定の場合はスキップ
                if not performer or not program:
                    continue

                result = ScrapingItem(
                    studio_name=studio_name,
                    start_time=datetime.datetime(
                        year=date.year, month=date.month, day=date.day, hour=hour, minute=minute, tzinfo=JST),
                    performer_name=performer,
                    program_name=program
                )
                result_list.append(result)

        date += datetime.timedelta(days=1)

    return result_list


def parse_schedule_to_performer_and_program(schedule_list: List[ScrapingItem]) -> tuple:
    performer_name_set = set()
    program_name_set = set()

    for schedule in schedule_list:
        performer_name_set.add(schedule.performer_name)
        program_name_set.add((schedule.performer_name, schedule.program_name))

    return performer_name_set, program_name_set
