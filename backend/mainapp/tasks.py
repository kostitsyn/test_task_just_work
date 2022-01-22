from celery import shared_task, Celery

# app = Celery('tasks', broker='pyamqp://guest@localhost//')
#
# @app.task
# def add(x, y):
#     return x + y


@shared_task
def add_counter(object):
    video_objects = object.video_objects.all()
    audio_objects = object.audio_objects.all()
    text_objects = object.text_objects.all()
    all_objects = sum([list(video_objects), list(audio_objects), list(text_objects)], [])
    for i in all_objects:
        i.counter += 1
        i.save()