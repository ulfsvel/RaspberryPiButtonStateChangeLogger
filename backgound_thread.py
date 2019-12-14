import queue
import threading

from logger import Logger


class BackgroundThread(threading.Thread):

    def __init__(self,
                 event_queue: queue.Queue,
                 db_credentials_secrets_store_arn,
                 db_cluster_arn, database_name
                 ):
        self._event_queue = event_queue
        self._db_credentials_secrets_store_arn = db_credentials_secrets_store_arn
        self._db_cluster_arn = db_cluster_arn
        self._database_name = database_name
        threading.Thread.__init__(self)

    def run(self):
        aurora_logger = Logger(
            self._db_credentials_secrets_store_arn,
            self._db_cluster_arn,
            self._database_name
        )
        while True:
            aurora_logger.log_event(self._event_queue.get())
