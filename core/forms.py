from django.forms import ModelForm, HiddenInput
from .models import MindMap


class MindMapForm(ModelForm):
   class Meta:
    model = MindMap
    fields = '__all__'
    widgets = {'content': HiddenInput()}
      