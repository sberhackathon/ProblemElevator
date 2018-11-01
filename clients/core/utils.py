from math import fabs
import core.constansts as cnt


# Functions not assigned to any class
def estimated_travel_time(from_floor, to_floor):
    return fabs(from_floor - to_floor) * cnt.time_between_floors


def max_client_wait_time(estimated_time, requests):
    max_time = 0  # Clicks

    for request in requests:
        diff = estimated_time - request.startTime
        if diff > max_time:
            max_time = diff

    return max_time
