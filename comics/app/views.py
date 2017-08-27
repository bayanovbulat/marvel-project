#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from app.models import ComicModel
from django.db import models
from django.core.paginator import Paginator, InvalidPage
import os
from django.views.decorators.csrf import csrf_exempt
from app.forms import ComicForm, ComicModelForm
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.edit import ProcessFormView
from django.core.urlresolvers import reverse
from django.views.generic.base import ContextMixin

from app.serializers import ComicSerializer
from rest_framework import viewsets

# Create your views here.
class ComicViewSet(viewsets.ModelViewSet):
    queryset = ComicModel.objects.all().order_by("name")
    serializer_class = ComicSerializer

@csrf_exempt
def search(request):
	comics = ComicModel.objects.all().order_by("name")
	try:
		page_num = request.GET["page"]
	except:
		page_num = 1
	if request.method == "POST":
		form = ComicForm(request.POST)
		if form.is_valid():
			comment = "not found"
			if ComicModel.objects.filter(name = request.POST['name']).exists():
				comic = ComicModel.objects.get(name = request.POST['name'])
				comic.in_stock = True
				comic.save()
				comment = "successfully"
			return render(request, "marvel.html", {"form": form, "pn": page_num, "comment": comment, "comics": comics})
		else:
			comment = "is not valid"
	else:
		form = ComicForm(request.POST)
		comment = "waiting"
	return render(request, "marvel.html", {"form": form, "pn": page_num, "comment": comment})
	
def name_image_get():
	images = ComicModel.objects.filter(cover__startswith = "app/static/")	
	s = [" " for i in range(0,images.count())]
	i = 0
	for image in images:
		if i == 0:
			s[i] = str(image.cover)
		else:
			s[i] = s[i] + str(image.cover)
		if s[i].find("app/static/pictures/") or s[i].find("app/static/"):
			s[i] = s[i].replace("pictures/","")
			s[i] = s[i].replace("app","")
		image.image_name = s[i]
		image.save()
		i = i + 1
	
class ComicListView(ListView):
	template_name = "base.html"
	queryset = ComicModel.objects.order_by("name")
	paginate_by = 5
	paginate_orphans = 1
	def get(self, request, *args, **kwargs):
		self.comics = ComicModel.objects.all()
		name_image_get()
		return super(ComicListView,self).get(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(ComicListView,self).get_context_data(**kwargs)
		context["comics"] = self.comics
		return context
	def get_queryset(self):
		return ComicModel.objects.order_by("name")

def list(request, view_id):
	name_image_get()
	try:
		page_num = request.GET["page"]
	except:
		page_num = 1
	paginator = Paginator(ComicModel.objects.filter(in_stock = True).order_by("name"), 5, orphans = 1)
	try:
		comics = paginator.page(page_num)
	except InvalidPage:
		comics = paginator.page(1)
	if view_id == "master":
		return render_to_response('base2.html', {'comics': comics})
	else:
		return render_to_response('base3.html', {'comics': comics})
		
class ComicUpdate(TemplateView):
	form = None
	template_name = "edit.html"
	def get(self, request, *args, **kwargs):
		self.form = ComicModelForm(instance = ComicModel.objects.get(pk = self.kwargs["id"]))
		return super(ComicUpdate, self).get(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(ComicUpdate, self).get_context_data(**kwargs)
		try:
			context["pn"] = self.request.GET["page"]
		except KeyError:
			context["pn"] = "1"
		context["comic"] = ComicModel.objects.get(pk = self.kwargs["id"])
		context["form"] = self.form
		return context
	def post(self, request, *args, **kwargs):
		comic = ComicModel.objects.get(pk = self.kwargs["id"])
		self.form = ComicModelForm(request.POST, instance = comic)
		if self.form.is_valid():
			self.form.save()
			return redirect("master")
		else:
			return super(ComicUpdate, self).post(request, *args, **kwargs)
			
class ComicDetailView(DetailView):
	template_name = "comic.html"
	model = ComicModel
	pk_url_kwarg = "id"
	fields = ['id', 'name', 'description', 'heroes_list', 'release_date', 'ean', 'type', 'cover', 'in_stock']
	def get_context_data(self, **kwargs):
		context = super(ComicDetailView,self).get_context_data(**kwargs)
		try:
			context["pn"] = self.request.GET["page"]
		except KeyError:
			context["pn"] = "1"
		try:
			context["comment"] = self.request.GET["comment"]
		except KeyError:
			context["comment"] = "2"
		context["comic"] = ComicModel.objects.get(pk = self.kwargs["id"])
		return context