"""
Scheduling of camera checking with threading.

"""
from threading import Thread
import time

from requests.exceptions import ReadTimeout, ConnectionError, HTTPError
import schedule

from camera_search import find_cameras
from text_request import text_message


def camera_check():
    try:
        found = find_cameras(target_condition=['9+', '9<'])
        if found:
            res = text_message(#debug=True,
                               message=f"Camera(s) found! {str(found)}")
            print(found)
            print(res.text)
        else:
            # log check
            print("Found nothing...")
    except (ConnectionError, ReadTimeout, HTTPError) as e:
        print(e)
        # log this


def create_schedule(job, *args, interval=15, units='minutes', **kwargs):
    """
    Create a scheduled job and pass args and kwargs to it.

    :job: function to be scheduled
    :interval: default time interval
    :units: default unit of time
    """
    sched = getattr(schedule.every(interval), units)
    sched.do(job, *args, **kwargs)


def threaded_schedule_run():
    """
    Keep checking for the schedule to be due and run it.
    """
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    create_schedule(camera_check,
                    # interval=15, # for test purposes only
                    # units='seconds')  # for test purposes only
                    interval=1, # for test purposes only
                    units='hours')

    # run the update now in it's own thread
    s = Thread(target=schedule.run_all())
    s.start()
    # thread the check for subsequent updates
    t = Thread(target=threaded_schedule_run)
    t.start()

