# coding: UTF-8
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

import datetime

class GlobalSiteSetting(models.Model):
  title = models.CharField(max_length=255, blank=True, null=False)
  description = models.CharField(max_length=255, blank=True, null=False)


class CMSUserManager(BaseUserManager):
  def _create_user(self, email, password=None, **extra_fields):
    if not email:
      raise ValueError('An E-mail address must be set.')

    email = CMSUserManager.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user


  def create_user(self, email, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', False)
    extra_fields.setdefault('is_superuser', False)
    return self._create_user(email, password, **extra_fields)
    

  def create_superuser(self, email, password, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    return self._create_user(username='admin', email=email, password=password, **extra_fields)


class CMSUser(AbstractBaseUser, PermissionsMixin):
  '''
  CMS User model derived by default User model
  '''

  username  = models.CharField(max_length=150, unique=True)
  screen_name = models.CharField(max_length=255, blank=False, null=False)
  email = models.EmailField(max_length=255, unique=True)

  first_name = models.CharField(max_length=255, null=True)
  last_name = models.CharField(max_length=255, null=True)

  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_superuser = models.BooleanField(default=False)
  date_joined = models.DateTimeField(null=True)
  
  USERNAME_FIELD = 'email'
  EMAIL_FIELD = 'email'

  objects = CMSUserManager()

  class Meta:
    db_table = 'mycms_cmsuser'
    swappable = 'AUTH_USER_MODEL'


class Article(models.Model):
  subject = models.CharField(max_length=1024, blank=False, null=False)
  body = models.TextField(blank=True, null=True)
  post_author = models.ForeignKey(CMSUser, on_delete=models.CASCADE)
  post_date = models.DateField(default=datetime.datetime.now)
