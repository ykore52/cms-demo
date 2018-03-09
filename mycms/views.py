# coding: UTF-8

from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.template import loader
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from .models import Article
from .models import CMSUser
from .models import GlobalSiteSetting

from .forms import CreateArticleForm, UpdateArticleForm

import re
from django.utils.html import strip_tags

from markdown2 import Markdown

def logout(request):
  template = loader.get_template('mycms/logout.html')
  return HttpResponse(template.render(request=request))

def convert_style(body):
  md = Markdown()
  return md.convert(strip_tags(body))


class IndexView(TemplateView):
  template_name = 'mycms/index.html'
  global_site_title = ""
  global_site_description = ""

  def global_site_setting(self):
    return GlobalSiteSetting.objects.get()

  def get_context_data(self, **kwargs):
    begin = 0
    context = super().get_context_data(**kwargs)
    context['past_num'] = begin
    return context

  def get_past_articles(self, begin):
    end = begin + 5
    return Article.objects \
        .select_related() \
        .order_by('post_date') \
        .reverse()[begin:end]

  def recent_articles(self):
    recent = Article.objects \
      .select_related() \
      .order_by('post_date') \
      .reverse()[0:5]

    for article in recent:
      article.body = convert_style(str(article.body))
    return recent


class PastArticleView(TemplateView):
  template_name = 'mycms/past_article.html'

  def get(self, request, *args, **kwargs):
    begin = kwargs['begin']

    if not re.match(r'^\d+$', begin):
      return HttpResponseRedirect(reverse('index'))

    begin = int(begin)
    if begin <= 0 or begin > 100000:
      return HttpResponseRedirect(reverse('index'), [])

    return super().get(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    begin = int(kwargs['begin'])
    context = super().get_context_data(**kwargs)
    context['past_articles'] = self.get_past_articles(begin * 5)
    context['past_num'] = begin
    return context

  def get_past_articles(self, begin):
    end = begin + 5
    return Article.objects \
        .select_related() \
        .order_by('post_date') \
        .reverse()[begin:end]


class MyPageView(TemplateView):
  template_name = 'mycms/mypage.html'

  def get_context_data(self, **kwargs):
    '''
    override get_content_data()
    '''
    context = super().get_context_data(**kwargs)
    context["all_articles"] = Article.objects.filter(post_author_id=self.request.user.id).order_by('id').reverse()
    return context



class ArticleView(DetailView):
  model = Article
  template_name = 'mycms/article.html'


  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    article = Article.objects.get(id=self.kwargs['pk'])
    article.body = convert_style(str(article.body))
    context['article'] = article

    return context


class CreateArticleView(CreateView):
  model = Article
  form_class = CreateArticleForm
  template_name = 'mycms/new_article.html'
  success_url = reverse_lazy('index')


class UpdateArticleView(UpdateView):
  model = Article
  form_class = UpdateArticleForm
  template_name = 'mycms/edit_article.html'
  success_url = reverse_lazy('index')

  def post(self, request, *args, **kwargs):
    self.object = self.get_object()
    form = self.get_form()
    if form.is_valid():
      update_article = form.save(commit=False)
      update_article.subject = self.request.POST.get('subject', False)
      update_article.body = self.request.POST.get('body', False)
      update_article.post_author = CMSUser.objects.get(id=self.request.user.id)
      update_article.save()
      return self.form_valid(form)
    else:
      return self.form_invalid(form)

  def form_valid(self, form):    
    return HttpResponseRedirect(self.get_success_url()) 

class DeleteArticleView(DeleteView):
  success_url = reverse_lazy('index')
  model = Article
