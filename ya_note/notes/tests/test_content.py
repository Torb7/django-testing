from notes.forms import NoteForm
from notes.tests.mixins import TestBaseClass
from notes.tests.constants import LIST_NOTES_URL, ADD_NOTE_URL, EDIT_NOTE_URL


class TestContent(TestBaseClass):

    def test_notes_list_for_different_users(self):
        url = LIST_NOTES_URL

        users_and_note_in_list = (
            (self.author_client, True),
            (self.not_author_client, False),
        )

        for auth_client, note_in_list in users_and_note_in_list:

            with self.subTest(user=auth_client, note_in_list=note_in_list):
                response = auth_client.get(url)

                object_list = response.context['object_list']
                self.assertIs((self.note in object_list), note_in_list)

    def test_pages_contains_form(self):
        urls = (ADD_NOTE_URL, EDIT_NOTE_URL)

        for url in urls:
            response = self.author_client.get(url)

            self.assertIn('form', response.context)

            self.assertIsInstance(response.context['form'], NoteForm)
