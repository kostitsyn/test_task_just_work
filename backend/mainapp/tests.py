import json
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient, APISimpleTestCase, APITestCase
from mixer.backend.django import mixer
from .views import PageModelViewSet, VideoModelViewSet, AudioModelViewSet, TextModelViewSet
from .models import Page, Video, Audio, Text



class TestVideoViewSet(APITestCase):

    def setUp(self) -> None:
        self.url = 'http://127.0.0.1:8000/api/video/'


    def test_get_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_object(self):
        video = Video.objects.create(title='test title',
                                     video_link='http://examplevideo.com',
                                     subtitles_link='http://exapmplesub.com')
        response = self.client.get(f'{self.url}{video.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_object(self):
        data = {
            'title': 'test title',
            'video_link': 'http://examplevideo.com',
            'subtitles_link': 'http://exapmplesub.com'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_object(self):
        video = Video.objects.create(title='test title',
                                     video_link='http://examplevideo.com',
                                     subtitles_link='http://exapmplesub.com')
        response = self.client.delete(f'{self.url}{video.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_edit_object(self):
        video = Video.objects.create(title='test title',
                                     video_link='http://examplevideo.com',
                                     subtitles_link='http://exapmplesub.com')
        new_title = 'new title'
        new_link = 'https://newvideo.org'
        updated_data = {
            'title': new_title,
            'video_link': new_link
        }
        response = self.client.patch(f'{self.url}{video.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], new_title)
        self.assertEqual(response.data['video_link'], new_link)


class TestAudioViewSet(APITestCase):
    def setUp(self) -> None:
        self.url = 'http://127.0.0.1:8000/api/audio/'

    def test_get_object(self):
        audio = Audio.objects.create(title='audio title', bitrate=128)
        response = self.client.get(f'{self.url}{audio.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['title'] == 'audio title')


class TestTextViewSet(APITestCase):
    def setUp(self) -> None:
        self.url = 'http://127.0.0.1:8000/api/text/'
        first_count_value = 1

    def test_get_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPageViewSet(APITestCase):
    def setUp(self) -> None:
        self.url = 'http://127.0.0.1:8000/api/pages/'

    def test_get_object(self):
        page = mixer.blend(Page)
        response = self.client.get(f'{self.url}{page.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_related_object_value(self):
        test_link = 'http://testvideolink.com'
        test_bitrate = 512
        test_text = 'test text'
        page = mixer.blend(
                           Page,
                           video_objects__video_link=test_link,
                           audio_objects__bitrate=test_bitrate,
                           text_objects__text=test_text
        )
        response = self.client.get(f'{self.url}{page.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['video_objects'][0]['video_link'], test_link)
        self.assertEqual(response.data['audio_objects'][0]['bitrate'], test_bitrate)
        self.assertEqual(response.data['text_objects'][0]['text'], test_text)

    def test_check_work_count(self):
        first_count_value = 1
        second_count_value = 2

        video_objects = mixer.cycle(3).blend(Video)
        audio_objects = mixer.cycle(4).blend(Audio)
        text_objects = mixer.cycle(2).blend(Text)

        page = mixer.blend(Page, video_objects=video_objects,
                           audio_objects=audio_objects,
                           text_objects=text_objects
                           )
        response = self.client.get(f'{self.url}{page.id}/')
        self.assertEqual(response.data['video_objects'][0]['counter'], first_count_value)

        response = self.client.get(f'{self.url}{page.id}/')
        self.assertEqual(response.data['video_objects'][0]['counter'], second_count_value)
