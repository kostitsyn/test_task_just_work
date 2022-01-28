from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from .serializers import PageSerializer, VideoSerializer, AudioSerializer, TextSerializer
from .models import Page, Video, Audio, Text
from rest_framework.response import Response
from .tasks import add_counter


class PageModelViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Page.objects.prefetch_related('video_objects', 'audio_objects', 'text_objects').all()
    serializer_class = PageSerializer
    search_fields = ['title']

    def retrieve(self, request, *args, pk=None):
        obj = Page.objects.get(pk=pk)
        add_counter.delay(pk)
        serializer_context = {'request': request}
        serializer = self.serializer_class(obj, context=serializer_context)
        return Response(serializer.data)


class BaseViewSet(ModelViewSet):
    search_fields = ['title']


class VideoModelViewSet(BaseViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class AudioModelViewSet(BaseViewSet):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer


class TextModelViewSet(BaseViewSet):
    queryset = Text.objects.all()
    serializer_class = TextSerializer
