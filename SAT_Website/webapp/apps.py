from django.apps import AppConfig
import os


class WebappConfig(AppConfig):
    name = 'webapp'

    def ready(self):
        from . import jobs

        if os.environ.get('RUN_MAIN', None) != 'true':
            print("Started scheduler.")
            jobs.start_scheduler()
