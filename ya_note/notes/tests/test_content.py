from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note
from notes.forms import NoteForm

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.not_author = User.objects.create(username='Не автор')

        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug='note-slug',
            author=cls.author,
        )

    def test_notes_list_for_different_users(self):
        url = reverse('notes:list')

        users_and_note_in_list = (
            (self.author, True),
            (self.not_author, False),
        )

        for user, note_in_list in users_and_note_in_list:
            self.client.force_login(user)

            with self.subTest(user=user, note_in_list=note_in_list):
                response = self.client.get(url)

                object_list = response.context['object_list']
                self.assertIs((self.note in object_list), note_in_list)

    def test_pages_contains_form(self):
        urls_with_args = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )

        for name, args in urls_with_args:
            url = reverse(name, args=args)

            self.client.force_login(self.author)
            response = self.client.get(url)

            self.assertIn('form', response.context)

            self.assertIsInstance(response.context['form'], NoteForm)
