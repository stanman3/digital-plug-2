from django.core.exceptions import ValidationError
from django.test import TestCase

from digital_plug_2.main.models import Project


class CreatorTests(TestCase):
    VALID_DATA = {
        'title': 'Lollimouth',
        'description': 'This is the description.',
    }

    def test_project_str__expect_to_display_title(self):
        project = Project(**self.VALID_DATA)
        expected = f'{self.VALID_DATA["title"]}'
        self.assertEqual(expected, project.__str__())