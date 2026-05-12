from django.urls import reverse

FORM_DATA = {
    'title': 'Новый заголовок',
    'text': 'Новый текст',
    'slug': 'new-slug',
}

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
