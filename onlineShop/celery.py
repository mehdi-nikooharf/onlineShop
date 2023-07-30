# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redismail.settings')
#
# app = Celery('redismail')
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
# app.conf.enable_utc = False
#
# app.conf.update(timezone = 'Europe/Paris')
#
# app.autodiscover_tasks()

from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlineShop.settings')

app = Celery('onlineShop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
