import json

import boto3

rds_client = boto3.client('rds-data', region_name='eu-west-1')

CREATE_QUERY = '''
CREATE TABLE IF NOT EXISTS `log` (
	`id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`event_type` VARCHAR(255) NOT NULL COLLATE 'utf8_bin',
	`event_data` MEDIUMTEXT NOT NULL COLLATE 'utf8_bin',
	`event_timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`)
)
COLLATE='utf8_bin'
ENGINE=InnoDB
;
'''

INSERT_QUERY = '''
INSERT INTO `log` (`event_type`, `event_data`) VALUES (:event_type, :event_data)
'''


class Logger:

    def __init__(self, db_credentials_secrets_store_arn, db_cluster_arn, database_name):
        self._db_credentials_secrets_store_arn = db_credentials_secrets_store_arn
        self._db_cluster_arn = db_cluster_arn
        self._database_name = database_name

    def _execute(self, sql, sql_parameters=None):
        if sql_parameters is None:
            sql_parameters = []

        rds_client.execute_statement(
            secretArn=self._db_credentials_secrets_store_arn,
            database=self._database_name,
            resourceArn=self._db_cluster_arn,
            sql=sql,
            parameters=sql_parameters
        )

    def create_log_table_if_not_exists(self):
        self._execute(CREATE_QUERY)

    def log_event(self, event: dict):
        self._execute(INSERT_QUERY, [
            {'name': 'event_type', 'value': {'stringValue': event.get("event_type")}},
            {'name': 'event_data', 'value': {'stringValue': json.dumps(event.get("event_data"))}}
        ])
