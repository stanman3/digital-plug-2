from django.test import TestCase
from digital_plug_2.main.models import Category


class CreatorTests(TestCase):
    VALID_DATA = {
        'name': 'Illustration',
    }

    def test_category_str__expect_to_display_name(self):
        category = Category(**self.VALID_DATA)
        expected = f'{self.VALID_DATA["name"]}'
        self.assertEqual(expected, category.__str__())