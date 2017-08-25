from django.contrib import admin
from app.models import ComicModel

# Register your models here.
class ComicModelAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'heroes_list', 'release_date', 'ean', 'type', 'cover', 'in_stock')
	search_fields = ('name', 'description', 'heroes_list', 'release_date', 'ean', 'type', 'cover', 'in_stock')

admin.site.register(ComicModel, ComicModelAdmin)