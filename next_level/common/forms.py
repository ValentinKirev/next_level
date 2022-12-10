from django import forms

from next_level.common.models import Comment
from next_level.utils import FormControlClassMixin


class BaseCommentForm(forms.ModelForm, FormControlClassMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_form_control_class()

    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Comment Text'
        }


class CommentCreateForm(BaseCommentForm):
    pass


class CommentEditForm(BaseCommentForm):
    pass


class SearchForm(forms.Form, FormControlClassMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = "Search"
        self.set_form_control_class()

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search by title',
            }
        )
    )
