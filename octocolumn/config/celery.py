import os
from celery import Celery

# `celery` 프로그램을 작동시키기 위한 기본 장고 세팅 값을 정한다.
# from config.settings import DEBUG

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.deploy')

# if DEBUG:
# app = Celery('config', backend='redis', broker='redis://127.0.0.1:6379/0')
# else:
app = Celery('config', backend='redis',
             broker='redis://A49gZTVTQ9uUpzX3m4B8ZnRTuUDKgV7PGimIxGTcuCo=@bycal.redis.cache.windows.net:6379')


# namespace='CELERY'는 모든 셀러리 관련 구성 키를 의미한다. 반드시 CELERY라는 접두사로 시작해야 한다.
app.config_from_object('django.conf:settings', namespace='CELERY')

# 장고 app config에 등록된 모든 taks 모듈을 불러온다.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))