import locale

from django.test import TestCase, LiveServerTestCase
from django.urls import reverse
from selenium.webdriver import Chrome, ChromeOptions
from pytz import timezone

from nepnep.settings import LOCALE_CODE, TIME_ZONE
from pearls.models import Post


class UnitTest(TestCase):
    fixtures = ['posts.json']

    def test_using_correct_templates(self):
        """Должны использоваться корректные шаблоны"""

        # Петя заходит на сайт
        response = self.client.get('/')
        # Петя сразу видит список постов
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'pearl_list.html')

    def test_posts_renders(self):
        """Посты должны отображаться на странице"""

        locale.setlocale(locale.LC_TIME, LOCALE_CODE)
        url = reverse('posts')

        # Петя заходит посмотреть посты
        response = self.client.get(url, HTTP_ACCEPT_LANGUAGE='ru')
        posts = Post.objects.all()
        page = response.content.decode('utf-8')
        for post in posts:
            time = post.created_at.astimezone(timezone(TIME_ZONE)).strftime('%H:%M %d %B %Y')
            # Петя должен увидеть каждый пост на странице
            self.assertIn(post.title, page)
            self.assertIn(post.description, page)
            self.assertIn(post.author.username, page)
            self.assertIn(time, page)


class FunctionalTest(LiveServerTestCase):
    def setUp(self):
        options = ChromeOptions()
        options.set_headless(True)
        self.browser = Chrome(options=options)

    def tearDown(self):
        self.browser.close()

    def test_title_is_correct(self):
        """В заголовке сайта должен упоминаться Nepnep"""

        # Петя заходит на сайт
        self.browser.get(self.live_server_url)
        # Петя должен понимать, что сайт называется Nepnep
        self.assertIn('Nepnep', self.browser.title)
