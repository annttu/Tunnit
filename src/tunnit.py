# encoding: utf-8

import logging
from datetime import datetime
import math
logger = logging.getLogger("Tunnit")


class Time(object):
    def __init__(self, t):
        self.t = t
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.days = 0
        self.set_time()

    def set_time(self):
        t = self.t.total_seconds()
        self.days = int(t / 86400)
        t = t - (self.days*86400)
        self.hours = int(t / 3600)
        t = t - (self.hours*3600)
        self.minutes = int(t / 60)
        self.seconds = t - (self.minutes*60)


def split_time(x):
    return Time(x)


def format_time(x):
    if not x:
        return "0d 0m"
    t = split_time(x)
    if t.days:
        return "%dd %dh %dm" % (t.days, t.hours, t.minutes)
    #if t.hours == 0 and t.minutes == 0:
    #    return "%dh %dm %ds" % (t.hours, t.minutes, t.seconds)
    return "%dh %dm" % (t.hours, t.minutes)


class Tunnit(object):
    def __init__(self):
        self.status = False
        self.timer = None
        self.description = ""
        self.stopped = None

    def toggle(self, description=None):
        if self.status:
            self.stop(description)
        else:
            self.start(description)

    def get_time(self):
        if not self.timer:
            return None
        return split_time(datetime.now() - self.timer)

    def get_formatted_time(self):
        if self.timer:
            if not self.stopped:
                t = datetime.now()
            else:
                t = self.stopped
            return format_time(t - self.timer)
        return format_time(None)

    def reset_timer(self):
        self.timer = None
        self.stopped = None

    def start(self, description=""):
        self.reset_timer()
        self.status = True
        self.description = description
        self.timer = datetime.now()
        logger.debug("Started working, %s" % description)

    def stop(self, description=None):
        if not self.status:
            return
        if description:
            self.description = description
        self.status = False
        time_spent = self.get_formatted_time()
        self.stopped = datetime.now()
        logger.info("Working stopped: %s, %s" % (time_spent, description))

