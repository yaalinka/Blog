from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from .models import *


class CustomLoginView(LoginView):
    template_name = 'page/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('main')


class RegisterPage(FormView):
    template_name = 'page/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('main')
        return super(RegisterPage, self).get(*args, **kwargs)


class MainPage(ListView):
    model = Article
    template_name = 'page/main.html'
    context_object_name = 'articles'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['cat_selected'] = None
        return context


class AddArticle(LoginRequiredMixin, CreateView):
    model = Article
    login_url = reverse_lazy('login')
    template_name = 'page/add_article.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.author = self.request.user
        data = self.request.POST
        if data['category'] != 'none':
            category = data['category']
        elif data['category_new']:
            category = data['category_new']
        form.instance.category, created = Category.objects.get_or_create(name=category)
        return super(AddArticle, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class Profile(LoginRequiredMixin, ListView):
    model = Article
    login_url = reverse_lazy('login')
    template_name = 'page/profile.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = context['articles'].filter(author=self.request.user)
        return context


class EditArticle(LoginRequiredMixin, UpdateView):
    model = Article
    login_url = reverse_lazy('login')
    template_name = 'page/add_article.html'
    slug_url_kwarg = 'article_slug'
    fields = ['title', 'content']
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.author = self.request.user
        data = self.request.POST
        if data['category'] != 'none':
            category = data['category']
        elif data['category_new']:
            category = data['category_new']
        form.instance.category, created = Category.objects.get_or_create(name=category)
        return super(EditArticle, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class DeleteArticle(LoginRequiredMixin, DeleteView):
    model = Article
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('profile')
    slug_url_kwarg = 'article_slug'


def ChosenCategory(request, pk):
    articles = Article.objects.filter(category__id=pk)
    cat_selected = Category.objects.get(id=pk)
    categories = Category.objects.exclude(id=pk)
    context = {'articles': articles, 'cat_selected': cat_selected, 'categories': categories}
    return render(request, 'page/main.html', context)


class ReadArticle(DetailView):
    model = Article
    template_name = 'page/article.html'
    slug_url_kwarg = 'article_slug'

