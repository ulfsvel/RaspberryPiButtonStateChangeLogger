import queue
import os
import logging

from backgound_thread import BackgroundThread
from detector import Detector
from logger import Logger
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
logging.basicConfig(level=int(os.environ.get("LOG_LEVEL")))

event_queue = queue.Queue()
event_logger = Logger(
    os.environ.get("SECRET_ARN"),
    os.environ.get("RDS_ARN"),
    os.environ.get("DB_NAME")
)
background_logger_thread = BackgroundThread(
    event_queue,
    os.environ.get("SECRET_ARN"),
    os.environ.get("RDS_ARN"),
    os.environ.get("DB_NAME")
)

logging.debug("Setting up RDS logging")
event_logger.create_log_table_if_not_exists()
logging.debug("RDS logging is set up")
logging.debug("Setting up event queue")
background_logger_thread.start()
logging.debug("Event queue is set up")


def handle_state_change(state):
    now = datetime.now()
    event = {
        "event_type": "DOOR_STATE_CHANGE",
        "event_data": {
            "device_time": now.strftime("%Y-%m-%d %H-%M-%S"),
            "device_state": "CLOSED" if state == Detector.STATE_PRESSED else "OPEN"
        }
    }
    event_queue.put(event)


change_detector = Detector(int(os.environ.get("GPIO_PIN")), handle_state_change)
change_detector.run()
