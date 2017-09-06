from django.conf.urls import url
from app.views import ComicListView, list, comics, search, ComicUpdate, ComicDetailView, Comic_UserDelete

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
	url(r'^all/$', ComicListView.as_view(), name = "all"),
	url(r'^marvel/$',  login_required(search), name = "marvel"),
	url(r'^master/$',  login_required(list), name = "master"),
	url(r'^comics/$', comics, name = "comics"),
	url(r'^comic/(?:(?P<id>\d+))$',   ComicDetailView.as_view(), name = "comic"),
	url(r'^master/(?P<id>\d+)/edit/$',  login_required(ComicUpdate.as_view()), name = "edit"),
	url(r'^master/(?P<id>\d+)/delete/$',  login_required(Comic_UserDelete.as_view()), name = "delete"),	
]