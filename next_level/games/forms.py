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
        exclude = ['author', 'publication_date_and_time', 'slug', 'status']
        labels = {
            'release_date': 'Release Date',
            'max_level': 'Max Level',
            'official_website': 'Official Website'
        }


class GameCreateForm(BaseGameForm):
    pass
