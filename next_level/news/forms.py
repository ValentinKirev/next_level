from django import forms

from next_level.news.models import NewsPost
from next_level.utils import FormControlClassMixin


class BaseNewsPostForm(forms.ModelForm, FormControlClassMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_form_control_class()

    class Meta:
        model = NewsPost
        exclude = ['author', 'publication_date_and_time', 'slug']
        labels = {
            'link_to_video': 'Link to Video'
        }


class NewsCreateForm(BaseNewsPostForm):
    pass


class NewsEditForm(BaseNewsPostForm):
    pass
