from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid


class Playbook(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    filename = models.CharField(max_length=255)
    playbook_dir = models.CharField(max_length=255, default='playbooks', blank=True, null=True)
    inventory = models.CharField(max_length=255)
    tags = models.ManyToManyField('Tag', blank=True)
    verbosity = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(4)],
        default=0
    )

    @property
    def run_command(self):
        tags = ''
        if self.tags.all():
            tags = '-t {}'.format(','.join([t.name for t in self.tags.all()]))

        vault_file = ''
        if settings.ANSIBLE_VAULT_FILE:
            vault_file = '--vault-password-file {}'\
                .format(settings.ANSIBLE_VAULT_FILE)

        if self.verbosity > 0:
            verbosity = '-' + ('v' * self.verbosity)

        return ' '.join([
            '{}/ansible-playbook'.format(settings.ANSIBLE_BIN_DIR),
            vault_file,
            '-i {}/inventories/{}'.format(
                settings.ANSIBLE_PROJECT_DIR, self.inventory),
            '{}/{}/{}'.format(
                settings.ANSIBLE_PROJECT_DIR,
                self.playbook_dir, self.filename),
            tags,
            verbosity
        ])

    def __str__(self):
        return '{} ({})'.format(self.name, self.id)


class Tag(models.Model):
    name = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    playbook = models.ForeignKey('Playbook', on_delete=models.PROTECT)
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=12,
        choices=[
            ('NOT_STARTED', 'NOT STARTED'),
            ('RUNNING', 'RUNNING'),
            ('SUCCESS', 'SUCCESS'),
            ('ERROR', 'ERROR')
        ],
        default='NOT_STARTED'
    )
    log = models.TextField(blank=True, null=True)
