from django.shortcuts import render,redirect
import os
from django.http import HttpResponse
from .forms import *
from .models import *
from django.contrib.auth.models import User
import uuid
from django.contrib import messages
from django.contrib.auth import authenticate
import time
import datetime
from datetime import timedelta
from django .views import generic
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# Create your views here.


class todoupload(generic.CreateView):
    form_class = todoform

    template_name = 'todoupload.html'
    success_url = reverse_lazy('tododisplay')

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(todoupload,self).form_valid(form)

class tododisplay(LoginRequiredMixin,generic.ListView):

    model = Task
    template_name = "tododisplay.html"
    context_object_name = 'a'

    # def get(self,request,**kwargs):
    #
    #     a=self.model.objects.all()
    #     return render(request,self.template_name,{"a":a})
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['a']=context['a'].filter(user=self.request.user)
        context['count']=context['a'].filter(complete=False).count()

        search_input=self.request.GET.get('search-area') or ''
        if search_input:
            context['a']=context['a'].filter(title__startswith=search_input)

        context["search_input"]= search_input
        return context


class tododetails(LoginRequiredMixin,generic.DetailView):
    template_name = 'tododetails.html'
    model = Task

class todoupdate(LoginRequiredMixin,generic.UpdateView):
    model = Task
    template_name = "todoupload.html"
    fields = ["title",'description','complete']
    success_url = reverse_lazy('tododisplay')

class tododelete(LoginRequiredMixin,generic.DeleteView):
    model = Task
    template_name = 'tododelete.html'
    success_url = reverse_lazy('tododisplay')


class CustomLoginView(LoginView):

    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    def get_success_url(self):




        return reverse_lazy('tododisplay')



class CustomRegister(generic.CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user=form.save()
        if user is not None:
            login(self.request,user)
        return super(CustomRegister,self).form_valid(form)



