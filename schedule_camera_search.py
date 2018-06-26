"""
Scheduling of camera checking.
"""
import time

from requests.exceptions import ReadTimeout, ConnectionError, HTTPError
import schedule

from camera_search import find_cameras, write_found_cameras
from text_request import text_message
import instance.config as config


def camera_check():
    try:
        found = find_cameras(target_condition=['9+', '9<'])
        # found = find_cameras(target_condition=['6', '8<']) # for testing
        if found:
            cameras = [str(f'{x[0]} @ {x[1]}') for x in found]
            response = text_message(debug=True,
                                    message=f"Camera(s) found! {cameras}")
            print(found)
            print(response.json()['body'])

        else:
            # log check
            print("Found nothing...")
    except (ConnectionError, ReadTimeout, HTTPError) as e:
        print(e)
        # log this
    else:
        # write id of camera to external file so message is not sent again
        found_cids = [x[2] for x in found]
        for c in found_cids:
            write_found_cameras(cid=c, filepath=config.file_location)


def create_schedule(job, *args, interval=15, units='minutes', **kwargs):
    """
    Create a scheduled job and pass args and kwargs to it.

    :job: function to be scheduled
    :interval: default time interval
    :units: default unit of time
    """
    sched = getattr(schedule.every(interval), units)
    sched.do(job, *args, **kwargs)


if __name__ == '__main__':
    create_schedule(camera_check,
                    # interval=15, # for test purposes only
                    # units='seconds')  # for test purposes only
                    interval=1,
                    units='hours')

    # run the update now
    schedule.run_all()

    while True:
        schedule.run_pending()
        time.sleep(1)
