import airflow
import pendulum

from airflow import DAG
from airflow.operators.python import PythonOperator
# from airflow.exceptions import AirflowSkipException
from airflow.operators.latest_only import LatestOnlyOperator


dag = DAG(
    dag_id="03_conditions_within_tasks",
    start_date=airflow.utils.dates.days_ago(1),
    schedule_interval="@hourly",
)

def _start():
    pass

def _fetch_weather():
    pass

def _clean_weather():
    pass

def _fetch_sales():
    pass

def _clean_sales():
    pass

def _join_datasets():
    pass

def _train_model():
    pass

def _deploy_model(**context):
    if context["execution_date"] == None:
        deploy_model()


start = PythonOperator(task_id="start", python_callable=_start, dag=dag)
fetch_weather = PythonOperator(task_id="fetch_weather", python_callable=_fetch_weather, dag=dag)
clean_weather = PythonOperator(task_id="clean_weather", python_callable=_clean_weather, dag=dag)
fetch_sales = PythonOperator(task_id="fetch_sales", python_callable=_fetch_sales, dag=dag)
clean_sales = PythonOperator(task_id="clean_sales", python_callable=_clean_sales, dag=dag)
join_datasets = PythonOperator(task_id="join_datasets", python_callable=_join_datasets, dag=dag)
train_model = PythonOperator(task_id="train_model", python_callable=_train_model, dag=dag)
deploy_model = PythonOperator(task_id="deploy_model", python_callable=_deploy_model, dag=dag)
latest_only = LatestOnlyOperator(task_id="latest_only", dag=dag)

start >> [fetch_weather, fetch_sales]
fetch_weather >> clean_weather
fetch_sales >> clean_sales
[clean_weather, clean_sales] >> join_datasets
join_datasets >> train_model
[train_model, latest_only] >> deploy_model