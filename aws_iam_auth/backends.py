from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
import base64
import json
import requests
import xmltodict
import logging

logger = logging.getLogger(__name__)

class AwsIamAuthentication(authentication.BaseAuthentication):
    @staticmethod
    def _parse_arn(arn):
        """Parses ARN string from XML response"""

        account_id = arn.split(':')[4]
        iam_type = arn.split(':')[5].split('/')[0]
        if iam_type == 'assumed-role':
            iam_type = 'role'
        iam_value = arn.split(':')[5].split('/')[1]
        return 'arn:aws:iam::{}:{}/{}'.format(account_id, iam_type, iam_value)

    @staticmethod
    def _retrieve_sts_response(auth_headers):
        """Retrieves the CallerIdentity from AWS STS and returns the XML response"""
        endpoint = 'https://sts.amazonaws.com'
        request_parameters = 'Action=GetCallerIdentity&Version=2011-06-15'
        request_url = endpoint + '?' + request_parameters

        try:
            r = requests.get(request_url, headers=auth_headers)
            if r.status_code != 200:
                message = xmltodict.parse(r.text)['ErrorResponse']['Error']['Message']
                raise exceptions.AuthenticationFailed('Could not validate the Caller Identity. Error: {}'.format(message))
            result = xmltodict.parse(r.text)['GetCallerIdentityResponse']['GetCallerIdentityResult']
        except Exception as e:
            raise(e)

        return result


    def authenticate(self, request):
        auth_headers = {
            'x-amz-date': request.META.get('HTTP_X_AMZ_DATE'),
            'x-amz-security-token': request.META.get('HTTP_X_AMZ_SECURITY_TOKEN'),
            'Authorization': request.META.get('HTTP_AUTHORIZATION')
        }
        result = self._retrieve_sts_response(auth_headers)

        arn = self._parse_arn(result['Arn'])

        user = None
        for u in settings.AWS_IAM_AUTH_ALLOWED_ARN_USER_MAPS:
            if arn == u['arn']:
                try:
                    user = User.objects.get(username=u['username'])
                except User.DoesNotExist as e:
                    logger.debug("Mapped user '{}' does not exist".format(u['username']))
                    raise exceptions.AuthenticationFailed('{} is not authorized.'.format(arn))
                break

        if not user:
            raise exceptions.AuthenticationFailed('{} is not authorized.'.format(arn))

        return user
