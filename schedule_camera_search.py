"""
Scheduling of camera checking.
"""
import logging
from logging.handlers import RotatingFileHandler
import time

from requests.exceptions import ReadTimeout, ConnectionError, HTTPError
import schedule

from camera_search import find_cameras, write_found_cameras
from text_request import text_message
import instance.config as config

log_stream_handler = logging.StreamHandler()
log_file_handler = RotatingFileHandler('logs/camera_search.log',
                                       maxBytes=10485760,  # 10MB
                                       backupCount=2)
logging.basicConfig(handlers=(log_stream_handler, log_file_handler),
                    level=logging.INFO,
                    format="%(asctime)s:%(levelname)s:%(message)s")


def camera_check(target_condition=None, debug=False):
    """
    Checks for new cameras and sends a text message if any are found.
    """
    try:
        found = find_cameras(target_condition)
        if found:
            cameras = [f"condition {x['condition']} @ {x['price']}"
                        for x in found]
            response = text_message(debug=debug,
                                    message=(f"Camera(s) found! {cameras} "
                                             "wexphotovideo.com/used-dslrs"))
            logging.debug(found)
            logging.info(f"Text message sent: {response.json()['body']}")
        else:
            logging.info("Found nothing...")
    except (ConnectionError, ReadTimeout, HTTPError) as e:
        logging.exception(e)
    else:
        if found:
            # write id of camera to external file so message is not sent again
            found_cids = [x['href'] for x in found]
            for c in found_cids:
                write_found_cameras(cid=c, filepath=config.file_location)
            logging.info(f'New found cameras written to file: {found_cids}')


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
                    # debug=True,  # for test purposes only
                    # target_condition=['9+', '8'],  # for test purposes only
                    # interval=15,  # for test purposes only
                    # units='seconds')  # for test purposes only
                    target_condition=['9+', '9'],
                    interval=30,
                    units='minutes')

    # run the update now
    schedule.run_all()

    while True:
        schedule.run_pending()
        time.sleep(1)
