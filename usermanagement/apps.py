from django.apps import AppConfig
from django.conf import settings
import redis
import django_rq
import threading

class UsermanagementConfig(AppConfig):
    name = 'usermanagement'
    redis_mail_cursor = redis.from_url(settings.REDIS_MAIL_URL)
    redis_limit_cursor = redis.from_url(settings.REDIS_LIMIT_URL)
    delay = settings.MAIL_DELAY

    def start_worker(self):
        worker = django_rq.get_worker('emails')
        worker.work()

    def ready(self):
        rc = self.redis_limit_cursor
        rc.set("max_mail_limit", settings.MAILING_LIMIT)
        rc.set("mails_left", settings.MAILING_LIMIT)
        

        
