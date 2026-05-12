from http import HTTPStatus

from pytils.translit import slugify

from notes.models import Note
from notes.forms import WARNING
from notes.tests.mixins import TestBaseClass
from notes.tests.constants import (
    ADD_NOTE_URL,
    EDIT_NOTE_URL,
    DELETE_NOTE_URL,
    EXPECTED_SUCCESS_URL,
    LOGIN_URL,
    FORM_DATA,
)


class TestLogic(TestBaseClass):

    def test_user_can_create_note(self):
        Note.objects.all().delete()

        url = ADD_NOTE_URL
        response = self.author_client.post(url, data=FORM_DATA)

        self.assertRedirects(response, EXPECTED_SUCCESS_URL)

        self.assertEqual(Note.objects.count(), 1)

        note = Note.objects.get()
        self.assertEqual(note.title, FORM_DATA['title'])
        self.assertEqual(note.text, FORM_DATA['text'])
        self.assertEqual(note.slug, FORM_DATA['slug'])
        self.assertEqual(note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        notes_count = Note.objects.count()

        url = ADD_NOTE_URL
        response = self.client.post(url, data=FORM_DATA)

        expected_url = f'{LOGIN_URL}?next={url}'
        self.assertRedirects(response, expected_url)

        self.assertEqual(Note.objects.count(), notes_count)

    def test_not_unique_slug(self):
        notes_count = Note.objects.count()

        FORM_DATA['slug'] = self.note.slug

        url = ADD_NOTE_URL
        response = self.author_client.post(url, data=FORM_DATA)

        self.assertFormError(
            response.context['form'], 'slug', errors=(self.note.slug + WARNING)
        )

        self.assertEqual(Note.objects.count(), notes_count)

    def test_empty_slug(self):
        notes_count = Note.objects.count()

        FORM_DATA.pop('slug')

        url = ADD_NOTE_URL
        response = self.author_client.post(url, data=FORM_DATA)

        self.assertRedirects(response, EXPECTED_SUCCESS_URL)

        self.assertEqual(Note.objects.count(), notes_count + 1)

        new_note = Note.objects.last()
        expected_slug = slugify(FORM_DATA['title'])
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_can_edit_note(self):
        url = EDIT_NOTE_URL
        response = self.author_client.post(url, data=FORM_DATA)

        self.assertRedirects(response, EXPECTED_SUCCESS_URL)

        note_from_db = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note_from_db.title, FORM_DATA['title'])
        self.assertEqual(note_from_db.text, FORM_DATA['text'])
        self.assertEqual(note_from_db.slug, FORM_DATA['slug'])
        self.assertEqual(note_from_db.author, self.author)

    def test_other_user_cant_edit_note(self):
        url = EDIT_NOTE_URL
        response = self.not_author_client.post(url, FORM_DATA)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        note_from_db = Note.objects.get(pk=self.note.pk)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(note_from_db.author, self.author)

    def test_author_can_delete_note(self):
        notes_count = Note.objects.count()

        url = DELETE_NOTE_URL
        response = self.author_client.post(url)

        self.assertRedirects(response, EXPECTED_SUCCESS_URL)

        self.assertEqual(Note.objects.count(), notes_count - 1)

    def test_other_user_cant_delete_note(self):
        notes_count = Note.objects.count()

        url = DELETE_NOTE_URL
        response = self.not_author_client.post(url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        self.assertEqual(Note.objects.count(), notes_count)
