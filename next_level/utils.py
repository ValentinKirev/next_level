class FormControlClassMixin:

    def set_form_control_class(self):
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class FormSelectClassMixin:
    select_fields = ()
    fields = {}

    def set_form_select_class(self):
        fields = self.select_fields

        for field_name in fields:
            field = self.fields[field_name]
            field.widget.attrs['class'] = 'form-select'
