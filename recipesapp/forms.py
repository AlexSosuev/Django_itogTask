from django import forms
from .models import Recipe, Category, RecipeCategoryRelationship

class RecipeForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'instructions', 'preparation_time', 'image', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control'}),
            'preparation_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'instructions': 'Инструкции',
            'preparation_time': 'Время приготовления (в минутах)',
            'image': 'Изображение',
            'category': 'Категория',
        }