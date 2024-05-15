from time import time


def days_to_seconds(days):
    return days * 24 * 60 * 60


def get_sub_day(get_time):
    return int(get_time) - int(time())
