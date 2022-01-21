from django.db import models


class Page(models.Model):
    title = models.CharField(max_length=256)
    video_objects = models.ManyToManyField('Video', related_name='pages')
    audio_objects = models.ManyToManyField('Audio', related_name='pages')
    text_objects = models.ManyToManyField('Text', related_name='pages')

    def __str__(self):
        return f'Page {self.title}'

    class Meta:
        ordering = ['-id']


class AbstractClass(models.Model):
    title = models.CharField(max_length=256)
    counter = models.IntegerField(default=0)

    class Meta:
        abstract = True


class Video(AbstractClass):
    video_link = models.URLField(max_length=512)
    subtitles_link = models.URLField(max_length=512)

    def __str__(self):
        return f'Video object {self.title}'

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Video objects'
        ordering = ['-id']


class Audio(AbstractClass):
    bitrate = models.IntegerField()

    def __str__(self):
        return f'Audio object {self.title}'

    class Meta:
        verbose_name = 'Audio'
        verbose_name_plural = 'Audio objects'
        ordering = ['-id']


class Text(AbstractClass):
    text = models.TextField()

    def __str__(self):
        return f'Text object {self.title}'

    class Meta:
        verbose_name = 'Text'
        verbose_name_plural = 'Text objects'
        ordering = ['-id']
