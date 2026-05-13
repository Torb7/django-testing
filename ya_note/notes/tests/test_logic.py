from http import HTTPStatus

from pytils.translit import slugify

from notes.models import Note
from notes.forms import WARNING
from notes.tests.base import (
    TestBaseClass,
    ADD_NOTE_URL,
    EDIT_NOTE_URL,
    DELETE_NOTE_URL,
    EXPECTED_SUCCESS_URL,
    LOGIN_URL,
)


class TestLogic(TestBaseClass):

    def test_user_can_create_note(self):
        Note.objects.all().delete()

        response = self.author_client.post(ADD_NOTE_URL, data=self.form_data)

        self.assertRedirects(response, EXPECTED_SUCCESS_URL)

        self.assertEqual(Note.objects.count(), 1)

        note = Note.objects.get()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        notes_count = Note.objects.count()

        response = self.client.post(ADD_NOTE_URL, data=self.form_data)

        expected_url = f'{LOGIN_URL}?next={ADD_NOTE_URL}'
        self.assertRedirects(response, expected_url)

        self.assertEqual(Note.objects.count(), notes_count)

    def test_not_unique_slug(self):
        notes_count = Note.objects.count()

        self.form_data['slug'] = self.note.slug

        response = self.author_client.post(ADD_NOTE_URL, data=self.form_data)

        self.assertFormError(
            response.context['form'], 'slug', errors=(self.note.slug + WARNING)
        )

        self.assertEqual(Note.objects.count(), notes_count)

    def test_empty_slug(self):
        Note.objects.all().delete()

        self.form_data.pop('slug')

        response = self.author_client.post(ADD_NOTE_URL, data=self.form_data)

        self.assertRedirects(response, EXPECTED_SUCCESS_URL)

        self.assertEqual(Note.objects.count(), 1)

        new_note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_can_edit_note(self):
        response = self.author_client.post(EDIT_NOTE_URL, data=self.form_data)

        self.assertRedirects(response, EXPECTED_SUCCESS_URL)

        note_from_db = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note_from_db.title, self.form_data['title'])
        self.assertEqual(note_from_db.text, self.form_data['text'])
        self.assertEqual(note_from_db.slug, self.form_data['slug'])
        self.assertEqual(note_from_db.author, self.author)

    def test_other_user_cant_edit_note(self):
        response = self.not_author_client.post(EDIT_NOTE_URL, self.form_data)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        note_from_db = Note.objects.get(pk=self.note.pk)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(note_from_db.author, self.author)

    def test_author_can_delete_note(self):
        notes_count = Note.objects.count()

        response = self.author_client.post(DELETE_NOTE_URL)

        self.assertRedirects(response, EXPECTED_SUCCESS_URL)

        self.assertEqual(Note.objects.count(), notes_count - 1)

    def test_other_user_cant_delete_note(self):
        notes_count = Note.objects.count()

        response = self.not_author_client.post(DELETE_NOTE_URL)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        self.assertEqual(Note.objects.count(), notes_count)
