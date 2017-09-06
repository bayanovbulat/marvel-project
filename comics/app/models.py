from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ComicModel(models.Model):
	class Meta:
		ordering = ["name","release_date"] #поля, по которым будет производиться сортировка
		verbose_name = "Comic" #название таблицы в ед.ч
		verbose_name_plural = "Comics" #название таблицы в мн.ч
	name = models.CharField(max_length = 100, unique = True, verbose_name = "Название")
	description = models.TextField(default = "Good comics!")
	heroes_list = models.TextField(default = "Good heroes!")
	release_date = models.DateField(verbose_name = "Дата выхода")
	ean = models.CharField(max_length = 25, verbose_name = "EAN")
	type = models.CharField(max_length = 25, verbose_name = "Варианты выхода")
	cover = models.ImageField(upload_to="app/static", verbose_name = "Обложка")
	in_stock = models.BooleanField(default = False, verbose_name = "Выбрать комикс")
	image_name = models.CharField(max_length = 100, editable = False, default = "")
	
class Comic_UserModel(models.Model):
	name = models.ForeignKey(User)
	product = models.ForeignKey(ComicModel, null = True, blank = True)