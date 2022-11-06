from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .forms import *
from .utils import *


class CatHome(DataMixin, ListView):
    model = Cat
    template_name = 'cats/index.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        context.update(c_def)
        return context

    def get_queryset(self):
        return Cat.objects.filter(is_published=True)


def about(request):
    return render(request, 'cats/about.html', {'title': 'О сайте', 'menu': menu})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'cats/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавить статью')
        context.update(c_def)
        return context


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


class ShowPost(DataMixin, DetailView):
    model = Cat
    template_name = 'cats/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        context.update(c_def)
        return context


class CatCategory(DataMixin, ListView):
    model = Cat
    template_name = 'cats/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].category),
                                      category_selected=context['posts'][0].category_id)
        context.update(c_def)
        return context

    def get_queryset(self):
        return Cat.objects.filter(category__slug=self.kwargs['category_slug'], is_published=True)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'cats/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        context.update(c_def)
        return context


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')