from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.utils.log.task_context_logger import logger

import logging
import sys
import os
# from speech.constants import DATA_FOLDER

staging_default_args = {
    'owner': 'ibrahim',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

@dag(
    default_args=staging_default_args,
    dag_id='orchestrator1123',
    description='Orchestrator operator',
    start_date=datetime(2021, 1, 1),
    tags=['orchestrator'],
    schedule=None,
)
def generate_dag():
    """
    DAG to:
    1. Get reddit posts from api via scrapper -> Kinesis
    2. Reddit posts from kinesis ->  turn them into mp3
    3.

    :return:
    """
    bash_task_1: BashOperator = BashOperator(task_id="hello", bash_command="echo hello")

    @task
    def task_2() -> None:
        logger.info("Ibrahim - task 2")
        # Log the PYTHONPATH environment variable
        logging.info(f"PYTHONPATH: {os.getenv('PYTHONPATH')}")

        # Log the current working directory
        logging.info(f"Current Working Directory: {os.getcwd()}")

        # Log the sys.path entries to check all accessible paths
        logging.info("sys.path entries:")
        for path in sys.path:
            logging.info(path)

        # Log the contents of /app to check if directories are mounted correctly
        try:
            app_contents = os.listdir("/app")
            logging.info("Contents of /app:")
            for item in app_contents:
                logging.info(item)
        except Exception as e:
            logging.error(f"Error accessing /app: {e}")

        # Test importing the speech module directly
        try:
            from speech.constants import DATA_FOLDER
            logging.info("Successfully imported speech.constants.DATA_FOLDER")
        except ImportError as e:
            logging.error(f"ImportError: {e}")

    bash_task_1 >> task_2()


generate_dag()
