from django.conf.urls import url
from app.views import ComicListView, list, search, ComicUpdate, ComicDetailView

urlpatterns = [
	url(r'^all/$', ComicListView.as_view(), name = "all"),
	url(r'^marvel/$', search, name = "marvel"),
	url(r'^master/$', list, {'view_id': 'master',}, name = "master"),
	url(r'^comics/$', list, {'view_id': 'comics',}, name = "comics"),
	url(r'^comic/(?:(?P<id>\d+))$', ComicDetailView.as_view(), name = "comic"),
	url(r'^master/(?P<id>\d+)/edit/$', ComicUpdate.as_view(), name = "edit"),
]