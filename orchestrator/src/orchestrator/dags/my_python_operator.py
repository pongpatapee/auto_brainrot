from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.utils.log.task_context_logger import logger

from orchestrator.tasks.polly_tts_task import polly_tts_task
from orchestrator.tasks.reddit_scraper_task import local_reddit_scraper_task


# from speech.constants import DATA_FOLDER

staging_default_args = {
    'owner': 'ibrahim',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

@dag(
    default_args=staging_default_args,
    dag_id='orchestrator',
    description='Orchestrator operator',
    start_date=datetime(2021, 1, 1),
    tags=['orchestrator'],
    schedule=None,
)
def generate_dag():
    """

    """
    bash_task_1: BashOperator = BashOperator(task_id="hello", bash_command="echo hello")

    @task
    def task_2() -> None:
        logger.info("Ibrahim - task 2  ")

    bash_task_1 >> task_2() >> local_reddit_scraper_task() >> polly_tts_task("test")


generate_dag()
