from .models import Page
from celery import shared_task


@shared_task
def add_counter(pk):
    obj = Page.objects.get(pk=pk)
    video_objects = obj.video_objects.all()
    audio_objects = obj.audio_objects.all()
    text_objects = obj.text_objects.all()
    all_objects = sum([list(video_objects), list(audio_objects), list(text_objects)], [])
    for i in all_objects:
        i.counter += 1
        i.save()
