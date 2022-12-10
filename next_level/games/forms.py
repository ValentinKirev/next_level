import html

from django import forms

from next_level.games.models import Game
from next_level.utils import FormControlClassMixin, FormSelectClassMixin


class BaseGameForm(forms.ModelForm, FormControlClassMixin, FormSelectClassMixin):
    select_fields = ['type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_form_control_class()
        self.set_form_select_class()

    class Meta:
        model = Game
        exclude = ['author', 'publication_date_and_time', 'slug', 'status', 'average_rating']
        labels = {
            'release_date': 'Release Date',
            'max_level': 'Max Level',
            'trailer': 'URL to Trailer',
            'official_website': 'Official Website'
        }

        widgets = {
            'release_date': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),
        }


class GameCreateForm(BaseGameForm):
    pass


class GameEditForm(BaseGameForm):
    pass


class FilterForm(forms.Form, FormControlClassMixin, FormSelectClassMixin):
    select_fields = ['sort_by', 'filter_by']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_form_control_class()
        self.set_form_select_class()

    DEFAULT=''
    MAX_LEVEL_ASCENDING = "Max Level " + html.unescape('&#8593;')
    MAX_LEVEL_DESCENDING = "Max Level " + html.unescape('&#8595;')
    RATING_ASCENDING = "Rating " + html.unescape('&#8593;')
    RATING_DESCENDING = "Rating " + html.unescape('&#8595;')
    RELEASE_DATE_ASCENDING = "Release Date " + html.unescape('&#8593;')
    RELEASE_DATE_DESCENDING = "Release Date " + html.unescape('&#8595;')

    SORT_CHOICES = [
        (DEFAULT, DEFAULT),
        (MAX_LEVEL_ASCENDING, MAX_LEVEL_ASCENDING),
        (MAX_LEVEL_DESCENDING, MAX_LEVEL_DESCENDING),
        (RATING_ASCENDING, RATING_ASCENDING),
        (RATING_DESCENDING, RATING_DESCENDING),
        (RELEASE_DATE_ASCENDING, RELEASE_DATE_ASCENDING),
        (RELEASE_DATE_DESCENDING, RELEASE_DATE_DESCENDING)
    ]

    FREE_TO_PLAY = 'Free To Play'
    PAY_TO_PLAY = 'Pay To Play'

    FILTER_CHOICES = [
        (DEFAULT, DEFAULT),
        (FREE_TO_PLAY, FREE_TO_PLAY),
        (PAY_TO_PLAY, PAY_TO_PLAY),
    ]

    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False
    )

    filter_by = forms.ChoiceField(
        choices=FILTER_CHOICES,
        required=False
    )
