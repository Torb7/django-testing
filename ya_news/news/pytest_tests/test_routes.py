from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('news:detail', pytest.lazy_fixture('news_pk_for_args')),
        ('users:login', None),
        ('users:signup', None),
        ('users:logout', None),
    ),
)
def test_pages_availability_for_anonymous_user(client, name, args):
    url = reverse(name, args=args)

    if name == 'users:logout':
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
@pytest.mark.parametrize('name', ('news:edit', 'news:delete'))
def test_pages_availability_for_different_users(
    parametrized_client, name, expected_status, comment
):
    url = reverse(name, args=(comment.pk,))
    response = parametrized_client.get(url)

    assert response.status_code == expected_status


@pytest.mark.parametrize('name', ('news:edit', 'news:delete'))
def test_redirects(client, name, comment_pk_for_args):
    login_url = reverse('users:login')

    url = reverse(name, args=comment_pk_for_args)
    response = client.get(url)

    expected_url = f'{login_url}?next={url}'

    assertRedirects(response, expected_url)
