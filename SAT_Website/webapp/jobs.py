from django.template.loader import render_to_string
from schedule import Scheduler
import threading
import time
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from string import Template
from .models import *

# global variables
current_site = Site.objects.get_current()
url = Template('$site/search/?q=$term&tweet_year=$year')


def send_email():
    emails = Email.objects.all().filter(EmailSent=False)
    # print(emails)

    for email in emails:
        print("Attempting to send email to", email.Email)


        # customize url for user
        # /search/?q=realDonaldTrump&tweet_year=2020
        term_o = Terms.objects.using('tweets').get(id=email.term_id)
        new_url = url.substitute(
            site=current_site.domain,
            term=term_o.term,
            year=term_o.year
        )

        if term_o.positivity is not None:
            email.EmailSent = True
            email.save()
            print("Positivity value exists. Sending!")
        else:
            print("Positivity value does not exist. Skipping!")
            continue

        html = render_to_string('email.html', {'url': new_url})

        send_mail(
            subject='Your query is ready to view!',
            from_email='sat.softeng1@gmail.com',
            recipient_list=[email.Email],
            fail_silently=False,
            html_message=html,
            message=""
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


# continuously run check for new emails to send
def start_scheduler():
    scheduler = Scheduler()
    scheduler.every().minute.at(':30').do(send_email)
    scheduler.run_continuously(300)
