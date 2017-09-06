#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from app.models import ComicModel, Comic_UserModel
from django.db import models
from django.core.paginator import Paginator, InvalidPage
import os
from django.views.decorators.csrf import csrf_exempt
from app.forms import ComicForm, ComicModelForm, LoginForm
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

from django.contrib.auth import authenticate, login, logout

# Create your views here.

class LoginView(TemplateView):
	form = None
	template_name = "login.html"
	def get(self, request, *args, **kwargs):
		self.form = LoginForm()
		return super(LoginView, self).get(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(LoginView, self).get_context_data(**kwargs)
		context["form"] = self.form
		return context
	def post(self,request,*args,**kwargs):
		self.form = LoginForm(request.POST)
		if self.form.is_valid():
			user = authenticate(username = self.form.cleaned_data["username"], password = self.form.cleaned_data["password"])
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect("master")
				else:
					return super(LoginView, self).get(request, *args, **kwargs)
			else:
				return super(LoginView, self).get(request, *args, **kwargs)
		else:
			return super(LoginView, self).get(request, *args, **kwargs)

class LogoutView(TemplateView):
	template_name = "logout.html"
	def get(self, request, *args, **kwargs):
		logout(request)
		return super(LogoutView, self).get(request, *args, **kwargs)

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
				comic = Comic_UserModel.objects.create(name = request.user, product = ComicModel.objects.get(name = request.POST['name']))
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
		self.users_comics = Comic_UserModel.objects.all()	
		name_image_get()
		return super(ComicListView,self).get(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(ComicListView,self).get_context_data(**kwargs)
		context["comics"] = self.comics
		return context
	def get_queryset(self):
		return ComicModel.objects.order_by("name")	
		
def list(request):
	comics = Comic_UserModel.objects.filter(name = request.user)
	try:
		page_num = request.GET["page"]
	except:
		page_num = 1
	paginator = Paginator(comics, 5, orphans = 1)
	try:
		pages = paginator.page(page_num)
	except InvalidPage:
		pages = paginator.page(1)
	return render_to_response('base2.html', {'comics': comics, 'pages': pages })

def comics(request):
	comics = Comic_UserModel.objects.all()
	try:
		page_num = request.GET["page"]
	except:
		page_num = 1
	paginator = Paginator(comics, 5, orphans = 1)
	try:
		pages = paginator.page(page_num)
	except InvalidPage:
		pages = paginator.page(1)
	return render_to_response('base3.html', {'comics': comics, 'pages': pages })
	
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
			return super(ComicUpdate, self).get(request, *args, **kwargs)

class Comic_UserDelete(DeleteView):
	model = Comic_UserModel
	template_name = "delete.html"
	pk_url_kwarg = "id"
	fields = ['name', 'product']
	def post(self, request, *args, **kwargs):
		self.success_url = reverse("master")
		return super(Comic_UserDelete, self).post(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(Comic_UserDelete, self).get_context_data(**kwargs)
		try:
			context["pn"] = self.request.GET["page"]
		except KeyError:
			context["pn"] = "1"
		context["current_comic"] = Comic_UserModel.objects.get(pk = self.kwargs["id"])
		return context
			
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