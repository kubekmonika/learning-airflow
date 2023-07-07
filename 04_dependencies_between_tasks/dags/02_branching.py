import airflow

from time import time
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator


dag = DAG(
    dag_id="branching",
    start_date=airflow.utils.dates.days_ago(1),
    schedule_interval="@hourly",
)

def _start():
    pass

def _fetch_weather():
    pass

def _clean_weather():
    pass

def _pick_erp_system(**context):
    """Branching operator returns the ID of the tasks that will be run"""
    # if context["execution_date"] < ERP_SWITCH_DATE:
    if time() % 2 > 1:
        return "fetch_sales_old"
    else:
        return "fetch_sales_new"

def _fetch_sales_old():
    pass

def _clean_sales_old():
    pass

def _fetch_sales_new():
    pass

def _clean_sales_new():
    pass

def _join_erp_branch():
    pass

def _join_datasets():
    pass

def _train_model():
    pass

def _deploy_model():
    pass


start = PythonOperator(task_id="start", python_callable=_start, dag=dag)
fetch_weather = PythonOperator(task_id="fetch_weather", python_callable=_fetch_weather, dag=dag)
clean_weather = PythonOperator(task_id="clean_weather", python_callable=_clean_weather, dag=dag)
pick_erp_system = BranchPythonOperator(
    task_id="pick_erp_system",
    python_callable=_pick_erp_system,
    dag=dag,
)
fetch_sales_old = PythonOperator(task_id="fetch_sales_old", python_callable=_fetch_sales_old, dag=dag)
clean_sales_old = PythonOperator(task_id="clean_sales_old", python_callable=_clean_sales_old, dag=dag)
fetch_sales_new = PythonOperator(task_id="fetch_sales_new", python_callable=_fetch_sales_new, dag=dag)
clean_sales_new = PythonOperator(task_id="clean_sales_new", python_callable=_clean_sales_new, dag=dag)
join_erp_branch = PythonOperator(
    task_id="join_erp_branch",
    python_callable=_join_erp_branch,
    trigger_rule="none_failed", # Add a "none_failed" trigger rule to allow the job to run when not all upstream tasks are succesfull
    dag=dag
)
join_datasets = PythonOperator(
    task_id="join_datasets",
    python_callable=_join_datasets,
    dag=dag,
)
train_model = PythonOperator(task_id="train_model", python_callable=_train_model, dag=dag)
deploy_model = PythonOperator(task_id="deploy_model", python_callable=_deploy_model, dag=dag)


start >> [pick_erp_system, fetch_weather]
fetch_weather >> clean_weather
pick_erp_system >> [fetch_sales_old, fetch_sales_new]
fetch_sales_old >> clean_sales_old
fetch_sales_new >> clean_sales_new
[clean_sales_old, clean_sales_new] >> join_erp_branch
[join_erp_branch, clean_weather] >> join_datasets
join_datasets >> train_model >> deploy_model
