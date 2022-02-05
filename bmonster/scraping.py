import datetime
import urllib.parse
from typing import List

import requests
from bs4 import BeautifulSoup

from bmonster.models import Studio, Performer, Program, Schedule

JST = datetime.timezone(datetime.timedelta(hours=9))
BASE_URL = "https://www.b-monster.jp"
PAGE_PATH = "reserve/"
URL = urllib.parse.urljoin(BASE_URL, PAGE_PATH)


def get_schedule_by_studio(
        studio_code: str, studio_name: str, now: datetime.datetime = datetime.datetime.now(JST)) -> List[dict]:

    result_list = []

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

                result = {
                    'studio_name': studio_name,
                    'start_time': datetime.datetime(
                        year=date.year, month=date.month, day=date.day, hour=hour, minute=minute, tzinfo=JST),
                    'performer': performer,
                    'program': program
                }
                result_list.append(result)

        date += datetime.timedelta(days=1)

    return result_list


def parse_schedule_to_performer_and_program(schedule_list: List[dict]) -> tuple:
    performer_set = set()
    program_set = set()

    for schedule in schedule_list:
        performer = schedule['performer']
        program = schedule['program']

        performer_set.add(performer)
        program_set.add((performer, program))

    return performer_set, program_set


def update_data():
    query_set = Studio.objects.all()
    performer_set = set()
    program_set = set()
    schedule_list = []
    for studio in query_set:
        studio_code = studio.code
        studio_name = studio.name
        schedule_list = get_schedule_by_studio(studio_code, studio_name)
        performer_set, program_set = parse_schedule_to_performer_and_program(schedule_list)

    for name in performer_set:
        try:
            performer = Performer.objects.get(name=name)
        except Performer.DoesNotExist:
            performer = Performer(name=name)
        performer.save()

    for item in program_set:
        performer_name = item[0]
        program_name = item[1]

        performer = Performer.objects.get(name=performer_name)

        try:
            program = Program.objects.get(performer=performer, name=program_name)
        except Program.DoesNotExist:
            program = Program(performer=performer, name=program_name)
        program.save()

    for item in schedule_list:
        studio_name = item['studio_name']
        start_time = item['start_time']
        performer_name = item['performer']
        program_name = item['program']

        studio = Studio.objects.get(name=studio_name)
        performer = Performer.objects.get(name=performer_name)
        program = Program.objects.get(performer=performer, name=program_name)

        try:
            schedule = Schedule.objects.get(studio=studio, start_time=start_time, performer=performer, program=program)
        except Schedule.DoesNotExist:
            schedule = Schedule(studio=studio, start_time=start_time, performer=performer, program=program)
        schedule.save()