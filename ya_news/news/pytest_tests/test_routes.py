from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

HOME_URL = pytest.lazy_fixture('home_url')
NEWS_DETAIL_URL = pytest.lazy_fixture('news_detail_url')
COMMENT_EDIT_URL = pytest.lazy_fixture('comment_edit_url')
COMMENT_DELETE_URL = pytest.lazy_fixture('comment_delete_url')
LOGIN_URL = pytest.lazy_fixture('login_url')
LOGOUT_URL = pytest.lazy_fixture('logout_url')
SIGNUP_URL = pytest.lazy_fixture('signup_url')


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url',
    (HOME_URL, NEWS_DETAIL_URL, LOGIN_URL, LOGOUT_URL, SIGNUP_URL),
)
def test_pages_availability_for_anonymous_user(client, url, logout_url):

    if url == logout_url:
        response = client.post(url)
    else:
        response = client.get(url)

    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
    ),
)
@pytest.mark.parametrize('url', (COMMENT_EDIT_URL, COMMENT_DELETE_URL))
def test_pages_availability_for_different_users(
    parametrized_client, expected_status, url
):
    response = parametrized_client.get(url)

    assert response.status_code == expected_status


@pytest.mark.parametrize('url', (COMMENT_EDIT_URL, COMMENT_DELETE_URL))
def test_redirects(client, url, login_url):
    response = client.get(url)

    expected_url = f'{login_url}?next={url}'

    assertRedirects(response, expected_url)
