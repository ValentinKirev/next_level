from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy


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


class UserOwnerMixin(object):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        try:
            user = self.get_object().user
        except AttributeError as ex:
            user = self.get_object().author

        if "Comment" in self.__class__.__name__:
            if user != request.user and not request.user.groups.filter(name__in=["Admin", "Staff"]).exists():
                return HttpResponseRedirect(reverse_lazy('index'))
        elif "Edit" in self.__class__.__name__:
            if user != request.user and not request.user.groups.filter(name__in=["Admin", "Staff"]).exists():
                return HttpResponseRedirect(reverse_lazy('index'))
        elif "Delete" in self.__class__.__name__:
            if user != request.user and not request.user.groups.filter(name__in=["Admin"]).exists():
                return HttpResponseRedirect(reverse_lazy('index'))

        return super().dispatch(request, *args, **kwargs)
