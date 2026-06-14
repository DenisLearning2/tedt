"""forms.py - Форма для создания проекта"""
from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    '''Форма для создания проекта'''
    # pylint: disable=too-few-public-methods
    class Meta:
        '''class Meta'''
        model = Project
        fields = ['name', 'description', 'github_url', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg',
                                           'placeholder': 'Название'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded-lg',
                                                 'placeholder': 'Описание'}),
            'github_url': forms.URLInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg',
                                                'placeholder': 'https://github.com/username/repo'}),
            'status': forms.Select(attrs={'class': 'w-full px-3 py-2 border rounded-lg'},),
        }
