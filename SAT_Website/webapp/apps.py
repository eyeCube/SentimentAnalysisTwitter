from django.apps import AppConfig
import os


# initialize scheduler as soon as we start our web app
class WebappConfig(AppConfig):
    name = 'webapp'

    def ready(self):
        from . import jobs

        # check for run_main to avoid conflicts
        if os.environ.get('RUN_MAIN', None) != 'true':
            print("Started scheduler.")
            jobs.start_scheduler()
