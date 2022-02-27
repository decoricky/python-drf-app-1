from django.test import TestCase

from bmonster import models
from bmonster.services import scraping


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
