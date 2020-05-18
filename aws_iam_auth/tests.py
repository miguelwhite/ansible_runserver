from django.test import TestCase, override_settings
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from unittest.mock import patch
from rest_framework import exceptions
from aws_iam_auth.backends import AwsIamAuthentication

@override_settings(
    AUTHENTICATION_BACKENDS=['aws_iam_auth.backends.AwsIamAuthentication'],
    AWS_IAM_AUTH_ALLOWED_ARN_USER_MAPS=[
        {
            'arn': 'arn:aws:iam::1234567890:user/testuser',
            'username': 'test'
        }
    ]
)
class AwsIamAuthenticationBackendTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@example.com', 'test')

    # Patch the method that actually makes the remote api call
    # to return a valid
    @patch.object(AwsIamAuthentication, '_retrieve_sts_response', return_value={
        "UserId": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "Account": "1234567890",
        "Arn": "arn:aws:iam::1234567890:user/testuser"
    })
    def test_authenticate_success(self, mock):
        """Test retrieving a valid user from AWS STS"""

        auth = AwsIamAuthentication()
        request = RequestFactory()
        self.assertEquals(
            auth.authenticate(request.get('/',
                HTTP_X_AMZ_DATE='foo',
                HTTP_X_AMZ_SECURITY_TOKEN='foo',
                HTTP_AUTHORIZATION='foo'
            )),
            self.user
        )

    # Patch the method that actually makes the remote api call
    # to return an invalid
    @patch.object(AwsIamAuthentication, '_retrieve_sts_response', return_value={
        "UserId": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "Account": "1234567890",
        "Arn": "arn:aws:iam::1234567890:user/baduser"
    })
    def test_authenticate_fail(self, mock):
        """Test retrieving unmapped user from AWS STS"""

        auth = AwsIamAuthentication()
        request = RequestFactory()
        with self.assertRaises(
            exceptions.AuthenticationFailed,
            msg='arn:aws:iam::1234567890:user/baduser is not authorized'
        ):
            auth.authenticate(request.get('/',
                HTTP_X_AMZ_DATE='foo',
                HTTP_X_AMZ_SECURITY_TOKEN='foo',
                HTTP_AUTHORIZATION='foo'
            ))
