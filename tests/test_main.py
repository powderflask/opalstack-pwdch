import unittest

from flask.ext.testing import TestCase
from project import app
from project.main.forms import RequestForm, PasswordResetForm
from project.token import generate_confirmation_token, confirm_token


#  TODO: mock API call for these tests to pass

class AppTestCase(TestCase):
    def create_app(self):
        app.config.from_object('project.config.TestingConfig')
        return app


class TestMainViews(AppTestCase):

    def test_correct_request_pw_reset_route(self):
        # Ensure login behaves correctly with correct credentials.
        with self.client:
            response = self.client.post(
                '/',
                data=dict(email="test@user.com", mailbox='test_user_com'),
                follow_redirects=True
            )
            self.assertTrue(response.status_code == 200)
            self.assertTemplateUsed('main/request_pwdch.html')

    def test_request_pw_reset_valid_token(self):
        # Ensure user can request a valid token.
        with self.client:
            self.client.post(
                '/',
                data=dict(email="test@user.com", mailbox='test_user_com'),
                follow_redirects=True)
            token = generate_confirmation_token('test@user.com')
            response = self.client.get('/reset/'+token, follow_redirects=True)
            self.assertTemplateUsed('main/reset_password.html')
            self.assertIn(
                b'You can now change your password.',
                response.data
            )

    def test_request_pw_reset_valid_token_correct_login(self):
        # Ensure user can use token to reset p/w.
        with self.client:
            self.client.post(
                '/',
                data=dict(email="test@user.com", mailbox='test_user_com'),
                follow_redirects=True)
            token = generate_confirmation_token('test@user.com')
            response = self.client.get('/reset/'+token, follow_redirects=True)
            self.assertIn(
                b'You can now change your password.',
                response.data
            )
            # test really starts herer
            response = self.client.post(
                '/reset/'+token,
                data=dict(password="New-p@ssw0rd", confirm="New-p@ssw0rd"),
                follow_redirects=True
            )
            self.assertIn(
                b'Password successfully changed.',
                response.data
            )

    # TODO: add test for invalid token response


class TestForms(AppTestCase):

    def test_validate_success_change_password_form(self):
        # Ensure correct data validates.
        form = PasswordResetForm(password='Abcd3 &gh1jk', confirm='Abcd3 &gh1jk')
        self.assertTrue(form.validate())

    def test_validate_invalid_change_password(self):
        # Ensure passwords must match.
        form = PasswordResetForm(password='update', confirm='unknown')
        self.assertFalse(form.validate())

    def test_validate_invalid_change_password_format(self):
        # Ensure invalid email format throws error.
        form = PasswordResetForm(password='abc123', confirm='abc123')
        self.assertFalse(form.validate())

    def test_validate_success_request(self):
        # Ensurevalid email format passes
        form = RequestForm(email='test@user.com', mailbox='test_user_com')
        self.assertTrue(form.validate())

    def test_validate_invalid_request_format(self):
        # Ensure invalid email format throws error.
        form = RequestForm(email='unknown', mailbox='test_user_com')
        self.assertFalse(form.validate())
        form = RequestForm(email='test@user.com', mailbox='abc')
        self.assertFalse(form.validate())

    def test_validate_invalid_request_no_such_user(self):
        # Ensure non-existent email / pw throws error.
        form = RequestForm(email='not@correct.com', mailbox='test_user_com')
        self.assertFalse(form.validate())
        form = RequestForm(email='test@user.com', mailbox='not_correct_com')
        self.assertFalse(form.validate())

if __name__ == '__main__':
    unittest.main()
