import datetime

from django.test import TestCase

from bmonster import scraping, models


class TestScraping(object):
    @classmethod
    def setup_class(cls):
        cls.studio_code = '0001'
        cls.studio_name = '銀座'

    def test_scraping_success(self):
        now = datetime.datetime(year=2022, month=1, day=21, hour=23, minute=58, second=59)
        result_list = scraping.get_schedule_by_studio(self.studio_code, self.studio_name, now)
        assert len(result_list) > 0

        now = datetime.datetime(year=2022, month=1, day=21, hour=0, minute=1, second=0)
        result_list = scraping.get_schedule_by_studio(self.studio_code, self.studio_name, now)
        assert len(result_list) > 0

    def test_scraping_skip(self):
        now = datetime.datetime(year=2022, month=1, day=21, hour=23, minute=59, second=0)
        result_list = scraping.get_schedule_by_studio(self.studio_code, self.studio_name, now)
        assert len(result_list) == 0

        now = datetime.datetime(year=2022, month=1, day=21, hour=0, minute=0, second=59)
        result_list = scraping.get_schedule_by_studio(self.studio_code, self.studio_name, now)
        assert len(result_list) == 0


class TestParseScheduleToPerformerAndProgram(object):
    @classmethod
    def setup_class(cls):
        studio_code = '0001'
        studio_name = '銀座'
        now = datetime.datetime(year=2022, month=1, day=21, hour=23, minute=58, second=59)
        cls.schedule_list = scraping.get_schedule_by_studio(studio_code, studio_name, now)

    def test_scraping_success(self):
        performer_set, program_set = scraping.parse_schedule_to_performer_and_program(self.schedule_list)
        assert len(performer_set) > 0
        assert len(program_set) > 0


class TestUpdateData(TestCase):
    def test_success(self):
        studio = models.Studio(code='0001', name='銀座')
        studio.save()
        query_set = models.Studio.objects.all()
        assert query_set.count() == 1

        scraping.update_data()

        query_set = models.Performer.objects.all()
        assert query_set.count() > 0

        query_set = models.Program.objects.all()
        assert query_set.count() > 0

        query_set = models.Schedule.objects.all()
        assert query_set.count() > 0
