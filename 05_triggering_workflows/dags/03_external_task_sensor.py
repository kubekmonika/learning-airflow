import datetime

import airflow.utils.dates
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.sensors.external_task import ExternalTaskSensor

dag1 = DAG(
    dag_id="03_external_task_sensor_dag_1",
    start_date=airflow.utils.dates.days_ago(5),
    schedule_interval="0 16 * * *",
)
dag2 = DAG(
    dag_id="03_external_task_sensor_dag_2",
    start_date=airflow.utils.dates.days_ago(5),
    schedule_interval="0 16 * * *",
)

EmptyOperator(task_id="copy_to_raw", dag=dag1) >> EmptyOperator(
    task_id="process_supermarket", dag=dag1
)

wait = ExternalTaskSensor(
    task_id="wait_for_process_supermarket",
    external_dag_id="03_external_task_sensor_dag_1",
    external_task_id="process_supermarket",
    execution_delta=datetime.timedelta(hours=6),
    dag=dag2,
)
report = EmptyOperator(task_id="report", dag=dag2)
wait >> report