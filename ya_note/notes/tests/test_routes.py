from http import HTTPStatus

from notes.tests.base import (
    TestBaseClass,
    HOME_URL,
    LIST_NOTES_URL,
    DETAIL_NOTE_URL,
    ADD_NOTE_URL,
    EDIT_NOTE_URL,
    DELETE_NOTE_URL,
    EXPECTED_SUCCESS_URL,
    LOGIN_URL,
    LOGOUT_URL,
    SIGNUP_URL,
)


class TestRoutes(TestBaseClass):

    def test_pages_availability(self):
        urls = (HOME_URL, LOGIN_URL, LOGOUT_URL, SIGNUP_URL)

        for url in urls:
            with self.subTest(url=url):
                if url == LOGOUT_URL:
                    response = self.client.post(url)
                else:
                    response = self.client.get(url)

                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_auth_user(self):
        urls = (LIST_NOTES_URL, ADD_NOTE_URL, EXPECTED_SUCCESS_URL)

        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)

                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_different_users(self):
        urls = (DETAIL_NOTE_URL, EDIT_NOTE_URL, DELETE_NOTE_URL)

        users_statuses = (
            (self.author_client, HTTPStatus.OK),
            (self.not_author_client, HTTPStatus.NOT_FOUND),
        )

        for auth_client, status in users_statuses:

            for url in urls:
                with self.subTest(user=auth_client, url=url):
                    response = auth_client.get(url)

                    self.assertEqual(response.status_code, status)

    def test_redirects(self):
        urls = (
            LIST_NOTES_URL,
            DETAIL_NOTE_URL,
            ADD_NOTE_URL,
            EDIT_NOTE_URL,
            DELETE_NOTE_URL,
            EXPECTED_SUCCESS_URL,
        )

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)

                expected_url = f'{LOGIN_URL}?next={url}'
                self.assertRedirects(response, expected_url)
