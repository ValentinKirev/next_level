from django import forms

from next_level.guides.models import GuideCategory, GuidePost
from next_level.utils import FormControlClassMixin


class BaseGuideCategoryForm(forms.ModelForm, FormControlClassMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_form_control_class()

    class Meta:
        model = GuideCategory
        exclude = ['author', 'publication_date_and_time', 'slug', 'updated_on', 'to_game']


class GuideCategoryCreateForm(BaseGuideCategoryForm):
    pass


class GuideCategoryEditForm(BaseGuideCategoryForm):
    pass


class BaseGuidePostForm(forms.ModelForm, FormControlClassMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_form_control_class()

    class Meta:
        model = GuidePost
        exclude = ['author', 'publication_date_and_time', 'slug', 'updated_on', 'to_category']


class GuidePostCreateForm(BaseGuidePostForm):
    pass


class GuidePostEditForm(BaseGuidePostForm):
    pass
