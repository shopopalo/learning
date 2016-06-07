from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module


# встраиваемая форма inlineformset_factory
# упрощает работу со связанными через внешний ключ объектами.
# В нашем случае упрощает работу с модулями, которые принадлежат одному курсу
ModuleFormSet = inlineformset_factory(Course,
                                      Module,
                                      # поля включенные в formset
                                      fields=['title', 'description'],
                                      # количество пустых форм Module
                                      extra=2,
                                      # параметр добавит checkbox, для указания
                                      # удалять форму или нет
                                      can_delete=True)


