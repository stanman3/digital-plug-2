from django.core.exceptions import ValidationError
from django.test import TestCase

from digital_plug_2.main.models import Creator


class CreatorTests(TestCase):
    VALID_DATA = {
        'first_name': 'Stan',
        'last_name': 'Manolov',
        'age': 15,
    }

    def test_creator_create__when_first_name_has_only_letters__expect_success(self):
        creator = Creator(**self.VALID_DATA)
        creator.save()
        self.assertIsNotNone(creator.pk)

    def test_creator_create__when_first_name_contains_digit__expect_fail(self):
        first_name = "stan1"
        creator = Creator(
            first_name=first_name,
            last_name='Manolov',
            age=15,
        )

        with self.assertRaises(ValidationError) as context:
            creator.full_clean()
            creator.save()

        self.assertIsNotNone(context.exception)

    def test_creator_create__when_first_name_contains_dollar_sign__expect_fail(self):
        first_name = "stan$"
        creator = Creator(
            first_name=first_name,
            last_name='Manolov',
            age=15,
        )

        with self.assertRaises(ValidationError) as context:
            creator.full_clean()
            creator.save()

        self.assertIsNotNone(context.exception)
