#!/usr/bin/env python
import os
import sys

# philpot
# per http://stackoverflow.com/questions/10339963/getdefaultlocale-returning-none-when-running-sync-db-on-django-project-in-pychar 
import os
os.environ['LANG'] = 'en_US.UTF-8'
os.environ['LC_ALL'] = 'en_US.UTF-8'

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Users.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
