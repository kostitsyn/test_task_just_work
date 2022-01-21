from celery import shared_task, Celery

# app = Celery('tasks', broker='pyamqp://guest@localhost//')
#
# @app.task
# def add(x, y):
#     return x + y


@shared_task
def add_counter(object):
    object.counter += 1
    object.save()