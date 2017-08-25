from django.conf.urls import url
from app.views import ComicListView, search, ComicListView2, ComicUpdate, ComicDetailView, ComicListView3, ComicDetailView2

urlpatterns = [
	url(r'^all/$', ComicListView.as_view(), name = "all"),
	url(r'^marvel/$', search, name = "marvel"),
	url(r'^master/$', ComicListView2.as_view(), name = "master"),
	url(r'^master/(?P<id>\d+)/edit/$', ComicUpdate.as_view(), name = "edit"),
	url(r'^master/(?:(?P<id>\d+))$', ComicDetailView.as_view(), name = "comic"),
	url(r'^comics/$', ComicListView3.as_view(), name = "comics"),
	url(r'^comics/(?:(?P<id>\d+))$', ComicDetailView2.as_view(), name = "comic2"),
]