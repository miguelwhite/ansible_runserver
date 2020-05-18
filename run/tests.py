from django.test import TestCase
from django.contrib.auth.models import User
from run.models import *
from run.management.commands.process_jobs import Command

class RunTest(TestCase):
    def setUp(self):
        # create a test playbook and user
        self.playbook = Playbook.objects.create(
            name='test playbook',
            description='test playbook',
            filename='test.yaml',
            inventory_filename='test.ini',
            verbosity=3
        )
        self.user = User.objects.create_superuser(
          'test',
          'test@example.com',
          'test'
        )

        # add Tags
        tag1 = Tag.objects.create(name='test_tag1')
        self.playbook.tags.add(tag1)
        tag2 = Tag.objects.create(name='test_tag2')
        self.playbook.tags.add(tag2)

        # add a Job
        Job.objects.create(
            playbook=self.playbook,
            requested_by=self.user
        )


    def test_playbook_run_command(self):
        """Playbook.run_command property"""

        self.assertEqual(self.playbook.run_command, (
            '/usr/local/bin/ansible-playbook '
            '--vault-password-file /home/test/.vault_pass '
            '-i /srv/ansiblesite/inventories/test.ini '
            '/srv/ansiblesite/playbooks/test.yaml '
            '-t test_tag1,test_tag2 -vvv'
        ))


    def test_process_job_created(self):
        """Playbook run is queued up"""

        self.assertEqual(Job.objects.filter(status='NOT_STARTED').count(), 1)


    def test_process_jobs_managemnt_command(self):
        """Test Command._process_jobs method"""

        Command._process_jobs(dry_run=True)

        self.assertEqual(Job.objects.filter(status='NOT_STARTED').count(), 0)

        processed_job = Job.objects.filter(status='SUCCESS').first()
        self.assertEqual(processed_job.log, '(DRY RUN) cmd: {}, cwd: {}'.format(
            self.playbook.run_command,
            '/srv/ansiblesite'
        ))
