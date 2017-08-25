from django import forms
from app.models import ComicModel
class ComicForm(forms.Form):
	name = forms.CharField(label = "Comic name",help_text = "")
	
class ComicModelForm(forms.ModelForm):
	class Meta:
		model = ComicModel
		fields = ['id', 'name', 'description', 'heroes_list', 'release_date', 'ean', 'type', 'cover', 'in_stock']
	name = forms.CharField(label = "Comic name",help_text = "must be unique")
	description = forms.CharField(widget = forms.Textarea, label = "description")
	heroes_list = forms.CharField(widget = forms.Textarea, label = "heroes_list")
	release_date = forms.DateField(label = "release date")
	ean = forms.CharField(label = "EAN")
	type = forms.CharField(label = "type release")
	cover = forms.ImageField(label = "image")
	in_stock = forms.BooleanField(required = False, label = "in stock")