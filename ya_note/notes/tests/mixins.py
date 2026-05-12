from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from notes.models import Note
from notes.tests.constants import NOTE_SLUG

User = get_user_model()


class TestBaseClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)

        cls.not_author = User.objects.create(username='Не автор')
        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.not_author)

        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug=NOTE_SLUG,
            author=cls.author,
        )
