from rest_framework import serializers

from app.models import ComicModel


class ComicSerializer(serializers.ModelSerializer):
	class Meta:
		model = ComicModel
		fields = ('id', 'name', 'description', 'heroes_list', 'release_date', 'ean', 'type', 'cover', 'in_stock', 'image_name')