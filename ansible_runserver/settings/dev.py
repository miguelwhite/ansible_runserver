from ansible_runserver.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'arse'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'arse_dev',
        'USER': 'arse',
        'PASSWORD': 'arse',
        'HOST': 'postgres',
        'PORT': '5432',
    }


}

ANSIBLE_PROJECT_DIR = ''  # path to dir with ansible playbooks
ANSIBLE_BIN_DIR = ''  # path to ansible binary
ANSIBLE_VAULT_FILE = os.environ.get('ANSIBLE_VAULT_PASSWORD_FILE')  # path to ansible vault password file
ANSIBLE_PROCESS_JOBS_FREQUENCY = 60  # Time in seconds between each process jobs query

# For dev use your current user
# shell command: aws sts get-caller-identity
AWS_IAM_AUTH_ALLOWED_ARN_USER_MAPS = [
    {
        'arn': 'arn:aws:iam::943976103640:user/mblanco2',
        'username': 'admin'
    }
]
"""
These dictionary maps allowed AWS IAM roles to django users
you have created.

AWS_IAM_AUTH_ALLOWED_ARN_USER_MAPS = [
    {
        'arn': 'arn:aws:iam::123456789:role/myrole',
        'username': 'my_django_user'
    }
]
"""
