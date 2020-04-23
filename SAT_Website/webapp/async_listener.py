from .streamlistener import listen
import os


def start_listener(*args):
    listener = listen(100, args)
    # print("Starting listener", os.getpid())
    while True:
        if listener.done:
            listener.print_tweets()
            break
    # print("Exiting listener")
