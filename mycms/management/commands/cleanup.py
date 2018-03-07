# coding: utf-8

from django.core.management.base import BaseCommand

import os
import subprocess
import shutil

class Command(BaseCommand):

  def handle(self, *args, **kwargs):
    project_home = os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), '../../../'))
    app_home = os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), '../../'))
    print('Clean up databases...')

    # rm -rf migrations/*.py
    try:
      shutil.rmtree(app_home + '/migrations/')
    except:
      pass
    finally:
      os.mkdir(app_home + '/migrations/')
      open(app_home + '/migrations/__init__.py', 'a').close()

    subprocess.call('python3 ' + project_home + '/manage.py makemigrations', shell=True)
    subprocess.call('python3 ' + project_home + '/manage.py migrate', shell=True)
