from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError
from django.urls import reverse

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

COMMENT_TEXT = 'Текст комментария'


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news_pk_for_args):
    url = reverse('news:detail', args=news_pk_for_args)
    form_data = {'text': COMMENT_TEXT}
    response = client.post(url, form_data)

    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)

    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(
    author_client, news, news_pk_for_args, author
):
    url = reverse('news:detail', args=news_pk_for_args)
    form_data = {'text': COMMENT_TEXT}
    response = author_client.post(url, form_data)

    assertRedirects(response, f'{url}#comments')

    comments_count = Comment.objects.count()
    assert comments_count == 1

    comment = Comment.objects.get()
    assert comment.text == COMMENT_TEXT
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, news_pk_for_args):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}

    url = reverse('news:detail', args=news_pk_for_args)
    response = author_client.post(url, data=bad_words_data)

    form = response.context['form']
    assertFormError(form=form, field='text', errors=WARNING)

    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.parametrize(
    'parametrized_client, expected_status, expected_comments_count',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.FOUND, 0),
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND, 1),
    ),
)
def test_deletion_comments_by_different_users(
    author_client,
    parametrized_client,
    expected_status,
    expected_comments_count,
    comment_pk_for_args,
    news_pk_for_args,
):
    delete_url = reverse('news:delete', args=comment_pk_for_args)
    response = parametrized_client.delete(delete_url)

    assert response.status_code == expected_status

    comments_count = Comment.objects.count()
    assert comments_count == expected_comments_count

    if parametrized_client is author_client:
        news_url = reverse('news:detail', args=news_pk_for_args)
        url_to_comments = news_url + '#comments'
        assertRedirects(response, url_to_comments)
