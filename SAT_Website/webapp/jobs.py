from schedule import Scheduler
import threading
import time
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from string import Template
from .models import *

current_site = Site.objects.get_current()
message = Template('You should be able to find your query here: $site/search/?q=$tweet')


def send_email():
    emails = Email.objects.all().filter(EmailSent=False)
    # print(emails)

    for email in emails:
        print("Attempting to send email to", email.Email)
        email.EmailSent = True
        email.save()

        m = message.substitute(site=current_site.domain, tweet=(Tweets.objects.using('tweets')
                               .get(id__exact=email.tweet_id)).text)
        # print(m)

        send_mail(
            'Your query is ready to view!',
            m,
            'sat.softeng1@gmail.com',
            [email.Email],
            fail_silently=False
        )


# this was taken from the scheduler API FAQ
def run_continuously(self, interval=1):
    """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @return cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    """

    cease_continuous_run = threading.Event()
    class ScheduleThread(threading.Thread):

        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run


Scheduler.run_continuously = run_continuously


def start_scheduler():
    scheduler = Scheduler()
    scheduler.every().minute.at(':30').do(send_email)
    scheduler.run_continuously(300)
