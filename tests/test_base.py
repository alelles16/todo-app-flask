from flask import url_for
from flask_testing import TestCase
from main import app


class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_auth_blueprint_available(self):
        self.assertIn('auth', self.app.blueprints)

    def test_login_get_available(self):
        response = self.client.get(url_for('auth.login'))
        self.assert200(response)

    def test_login_template_available(self):
        self.client.get(url_for('auth.login'))
        self.assertTemplateUsed('login.html')

    def test_auth_login_post(self):
        fake_form = {
            'username': 'fake',
            'password': 'fakepass'
        }
        response = self.client.post(url_for('auth.login'), data=fake_form)
        self.assertRedirects(response, url_for('auth.me'))
