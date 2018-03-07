from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import GlobalSiteSetting
from .models import Article
from .models import CMSUser

admin.site.register(GlobalSiteSetting)
admin.site.register(Article)

from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CMSUser
from django import forms


class CMSUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CMSUser


class CMSUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CMSUser

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            CMSUser.objects.get(username=username)
        except CMSUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


class CMSUserAdmin(UserAdmin):
    form = CMSUserChangeForm
    add_form = CMSUserCreationForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('screen_name', )}),
    )

admin.site.register(CMSUser, CMSUserAdmin)