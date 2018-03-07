from django import forms

from .models import Article

class CreateArticleForm(forms.ModelForm):
  """
  """
  
  class Meta:
    model = Article
    fields = ['subject', 'body', 'post_author']  

class UpdateArticleForm(forms.ModelForm):
  """
  """
  
  class Meta:
    model = Article
    fields = ['subject', 'body']