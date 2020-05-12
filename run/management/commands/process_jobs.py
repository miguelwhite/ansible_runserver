from django.core.management.base import BaseCommand, CommandError
from run.models import Job
from django.conf import settings

import subprocess
import logging
import time
import sys
import signal

logging.basicConfig(
     format='%(asctime)s %(levelname)-8s %(message)s',
     level=logging.INFO,
     datefmt='%Y-%m-%d %H:%M:%S')


class SigtermHandler:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        print('Exiting gracefully...')
        self.kill_now = True


class Command(BaseCommand):
    help = 'Process Job Daemon'

    def _process_jobs(self):
        logging.info('Getting queued jobs')
        jobs = Job.objects.filter(status='NOT_STARTED').order_by('-created_on')
        if len(jobs) == 0:
            logging.info('No queued jobs')
        else:
            for job in jobs:
                output = ''
                try:
                    job.status = 'RUNNING'
                    job.save()
                    logging.info(
                        'Job id {}: playbook run start'.format(job.id)
                    )
                    run_command = job.playbook.run_command
                    output = subprocess.check_output(
                        run_command,
                        cwd=settings.ANSIBLE_PROJECT_DIR,
                        stderr=subprocess.STDOUT,
                        shell=True
                    )
                    job.status = 'SUCCESS'
                    if type(output) == 'bytes':
                        job.log = output.decode("utf-8")
                    else:
                        job.log = output
                    logging.info('Job id {}: playbook run end'.format(job.id))
                except subprocess.CalledProcessError as e:
                    logging.error('Job id {}: {}'.format(job.id, str(e)))
                    job.log = e.output.decode("utf-8")
                    job.status = 'ERROR'
                except Exception as e:
                    logging.error('Job id {}: {}'.format(job.id, str(e)))
                    job.log = 'Error processing job. Please check the run server.'
                    job.status = 'ERROR'
                finally:
                    job.save()

    def handle(self, *args, **options):
        sigterm_handler = SigtermHandler()
        while not sigterm_handler.kill_now:
            try:
                self._process_jobs()
                time.sleep(settings.ANSIBLE_PROCESS_JOBS_FREQUENCY)
            except KeyboardInterrupt:
                print('Exiting...')
                sys.exit()
