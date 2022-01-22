from rest_framework.serializers import HyperlinkedModelSerializer
from .models import Page, Video, Audio, Text


class VideoSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class AudioSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Audio
        fields = '__all__'


class TextSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Text
        fields = '__all__'


class PageSerializer(HyperlinkedModelSerializer):
    video_objects = VideoSerializer(many=True)
    audio_objects = AudioSerializer(many=True)
    text_objects = TextSerializer(many=True)

    class Meta:
        model = Page
        fields = '__all__'