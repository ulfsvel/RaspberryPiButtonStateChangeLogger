import queue
import threading

from logger import Logger


class BackgroundThread(threading.Thread):

    def __init__(self,
                 event_queue: queue.Queue,
                 db_credentials_secrets_store_arn,
                 db_cluster_arn, database_name,
                 aws_access_key,
                 aws_secret_access_key
                 ):
        self._event_queue = event_queue
        self._db_credentials_secrets_store_arn = db_credentials_secrets_store_arn
        self._db_cluster_arn = db_cluster_arn
        self._database_name = database_name
        self._aws_access_key = aws_access_key
        self._aws_secret_access_key = aws_secret_access_key
        threading.Thread.__init__(self)

    def run(self):
        aurora_logger = Logger(
            self._db_credentials_secrets_store_arn,
            self._db_cluster_arn,
            self._database_name,
            self._aws_access_key,
            self._aws_secret_access_key
        )
        while True:
            aurora_logger.log_event(self._event_queue.get())
