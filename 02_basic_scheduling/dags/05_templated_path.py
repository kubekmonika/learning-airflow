import datetime as dt
from pathlib import Path
import pandas as pd

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


def _calculate_stats(**context):
    """Calculates event statistics."""

    input_path = context["templates_dict"]["input_path"]
    output_path = context["templates_dict"]["output_path"]

    Path(output_path).parent.mkdir(exist_ok=True)

    events = pd.read_json(input_path)
    stats = events.groupby(["date", "user"]).size().reset_index()
    stats.to_csv(output_path, index=False)


dag = DAG(
    dag_id="05_templated_path",
    start_date=dt.datetime(2023, 6, 15),
    end_date=dt.datetime(2023, 6, 20),
    schedule_interval='@daily',
)

fetch_events = BashOperator(
    task_id="fetch_events",
    bash_command=(
        "mkdir -p /data && "
        "curl -o /data/events/{{ds}}.json "
        "http://localhost:5000/events?"
        "start_date={{execution_date.strftime('%Y-%m-%d')}}"
        "&end_date={{next_execution_date.strftime('%Y-%m-%d')}}"
        # alternative solution:
        # "start_date={{ds}}&"
        # "end_date={{next_ds}}"
    ),
    dag=dag,
)

calculate_stats = PythonOperator(
    task_id="calculate_stats",
    python_callable=_calculate_stats,
    templates_dict={
        "input_path": "/data/events/{{ds}}.json",
        "output_path": "/data/stats/{{ds}}.csv",
    },
    dag=dag,
)

fetch_events >> calculate_stats
