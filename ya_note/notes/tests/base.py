from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note

User = get_user_model()

NOTE_SLUG = 'note-slug'

HOME_URL = reverse('notes:home')
LIST_NOTES_URL = reverse('notes:list')
DETAIL_NOTE_URL = reverse('notes:detail', args=(NOTE_SLUG,))
ADD_NOTE_URL = reverse('notes:add')
EDIT_NOTE_URL = reverse('notes:edit', args=(NOTE_SLUG,))
DELETE_NOTE_URL = reverse('notes:delete', args=(NOTE_SLUG,))
EXPECTED_SUCCESS_URL = reverse('notes:success')
LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')


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

        cls.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'new-slug',
        }
