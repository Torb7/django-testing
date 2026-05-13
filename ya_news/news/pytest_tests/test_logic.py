from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

FORM_DATA = {'text': 'Новый текст комментария'}
BAD_WORDS_DATA = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
    client, news_detail_url, login_url
):
    response = client.post(news_detail_url, FORM_DATA)

    expected_url = f'{login_url}?next={news_detail_url}'
    assertRedirects(response, expected_url)

    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(author_client, news, news_detail_url, author):
    response = author_client.post(news_detail_url, FORM_DATA)

    assertRedirects(response, f'{news_detail_url}#comments')

    comments_count = Comment.objects.count()
    assert comments_count == 1

    comment_from_db = Comment.objects.get()
    assert comment_from_db.text == FORM_DATA['text']
    assert comment_from_db.news == news
    assert comment_from_db.author == author


def test_user_cant_use_bad_words(author_client, news_detail_url):
    response = author_client.post(news_detail_url, data=BAD_WORDS_DATA)

    form = response.context['form']
    assertFormError(form=form, field='text', errors=WARNING)

    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(
    author_client, comment_delete_url, news_detail_url
):
    response = author_client.delete(comment_delete_url)

    url_to_comments = news_detail_url + '#comments'
    assertRedirects(response, url_to_comments)

    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_delete_comment_of_another_user(
    not_author_client, comment_delete_url
):
    response = not_author_client.delete(comment_delete_url)

    assert response.status_code == HTTPStatus.NOT_FOUND

    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_edit_comment(
    author_client, comment, comment_edit_url, news_detail_url
):
    response = author_client.post(comment_edit_url, data=FORM_DATA)

    url_to_comments = news_detail_url + '#comments'
    assertRedirects(response, url_to_comments)

    comment_from_db = Comment.objects.get(pk=comment.pk)
    assert comment_from_db.text == FORM_DATA['text']
    assert comment_from_db.news == comment.news
    assert comment_from_db.author == comment.author


def test_user_cant_edit_comment_of_another_user(
    not_author_client, comment, comment_edit_url
):
    response = not_author_client.post(comment_edit_url, data=FORM_DATA)

    assert response.status_code == HTTPStatus.NOT_FOUND

    comment_from_db = Comment.objects.get(pk=comment.pk)
    assert comment_from_db.text == comment.text
    assert comment_from_db.news == comment.news
    assert comment_from_db.author == comment.author
