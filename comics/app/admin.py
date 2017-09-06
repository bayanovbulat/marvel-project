from django.contrib import admin
from app.models import ComicModel, Comic_UserModel

# Register your models here.
class ComicModelAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'heroes_list', 'release_date', 'ean', 'type', 'cover', 'in_stock')
	search_fields = ('name', 'description', 'heroes_list', 'release_date', 'ean', 'type', 'cover', 'in_stock')

class Comic_UserModelAdmin(admin.ModelAdmin):
	list_display = ('name', 'product')
	search_fields = ('name', 'product')
	
admin.site.register(ComicModel, ComicModelAdmin)
admin.site.register(Comic_UserModel, Comic_UserModelAdmin)