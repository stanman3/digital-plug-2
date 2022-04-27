from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from digital_plug_2.main.validators import MaxFileSizeInMbValidator, validate_only_letter


class Creator(models.Model):
    FIRST_NAME_MIN_LEN = 2
    FIRST_NAME_MAX_LEN = 15

    LAST_NAME_MIN_LEN = 2
    LAST_NAME_MAX_LEN = 15

    LOCATION_MIN_LEN = 2
    LOCATION_MAX_LEN = 15

    PASS_MIN_LEN = 8
    PASS_MAX_LEN = 15

    AGE_MIN_VALUE = 13

    IMAGE_MAX_SIZE_IN_MB = 5
    IMAGE_UPLOAD_TO_DIR = 'profiles/'

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LEN,
        null=True,
        blank=True,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LEN),
            validate_only_letter,
        ),
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LEN,
        null=True,
        blank=True,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LEN),
            validate_only_letter,
        ),
    )

    age = models.IntegerField(
        null=True,
        blank=True,
        validators=(
            MinValueValidator(AGE_MIN_VALUE),
        ),
    )

    email = models.EmailField(
        null=True,
        blank=True,
    )

    country = models.CharField(
        max_length=LOCATION_MAX_LEN,
        null=True,
        blank=True,
        validators=(
            MinLengthValidator(LOCATION_MIN_LEN),
            validate_only_letter,
        ),
    )

    image = models.ImageField(
        upload_to=IMAGE_UPLOAD_TO_DIR,
        null=True,
        blank=True,
        validators=(
            MaxFileSizeInMbValidator(IMAGE_MAX_SIZE_IN_MB),
        )
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Category(models.Model):
    CAT_MAX_LEN = 20

    name = models.CharField(
        max_length=CAT_MAX_LEN,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Project(models.Model):
    ILL = 'Illustration'
    TYPO = 'Typography'
    LOGOS = 'Logos'

    CATEG = [(x, x) for x in (ILL, TYPO, LOGOS)]

    TITLE_MAX_LENGTH = 15

    IMAGE_MAX_SIZE_IN_MB = 5
    IMAGE_UPLOAD_TO_DIR = 'projects/'

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
    )

    # category = models.CharField(
    #     max_length=max(len(x) for (x, _) in CATEG),
    #     choices=CATEG,
    # )

    category = models.ManyToManyField(Category)

    description = models.TextField()

    image = models.ImageField(
        upload_to=IMAGE_UPLOAD_TO_DIR,
        null=True,
        blank=True,
        validators=(
            MaxFileSizeInMbValidator(IMAGE_MAX_SIZE_IN_MB),
        )
    )

    creator = models.ForeignKey(Creator, null=True, on_delete=models.CASCADE,)

    def __str__(self):
        return self.title
