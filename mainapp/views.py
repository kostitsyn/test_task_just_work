from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from .serializers import PageSerializer, VideoSerializer, AudioSerializer, TextSerializer
from .models import Page, Video, Audio, Text
from rest_framework.response import Response
from .tasks import add_counter


class PageModelViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['^title']
    ordering_fields = ['video_objects', 'audio_objects', 'text_objects']
    # ordering = ['text_objects', 'video_objects', 'audio_objects']


class BaseViewSet(ModelViewSet):
    filter_backends = (SearchFilter,)
    search_fields = ['^title']

    def retrieve(self, request, pk=None):
        data_type = self.basename
        if data_type == 'video':
            entity = Video
            serializer_class = VideoSerializer
        elif data_type == 'audio':
            entity = Audio
            serializer_class = AudioSerializer
        elif data_type == 'text':
            entity = Text
            serializer_class = TextSerializer
        obj = entity.objects.get(pk=pk)
        add_counter(obj)
        serializer_context = {'request': request}
        serializer = serializer_class(obj, context=serializer_context)
        return Response(serializer.data)


class VideoModelViewSet(BaseViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class AudioModelViewSet(BaseViewSet):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer


class TextModelViewSet(BaseViewSet):
    queryset = Text.objects.all()
    serializer_class = TextSerializer
