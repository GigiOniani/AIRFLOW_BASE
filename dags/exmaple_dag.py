"""Example DAG demonstrating the usage of the PythonOperator."""
import time
from pprint import pprint

from airflow import DAG
from airflow.operators.python import PythonOperator, PythonVirtualenvOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow',
}

dag = DAG(
    dag_id='example_python_operator',
    default_args=args,
    catchup=False,
    schedule_interval=None,
    start_date=days_ago(2),
    tags=['example'],
)


def print_context(ds, **kwargs):
    """Print the Airflow context and ds variable from the context."""

    pprint(kwargs)
    print(ds)
    return 'Whatever you return gets printed in the logs'


run_this = PythonOperator(
    task_id='print_the_context',
    python_callable=print_context,
    dag=dag,
)


def my_sleeping_function(random_base):
    """This is a function that will run within the DAG execution"""

    time.sleep(random_base)


for i in range(5):
    task = PythonOperator(
        task_id='sleep_for_' + str(i),
        python_callable=my_sleeping_function,
        op_kwargs={'random_base': float(i) / 10},
        dag=dag,
    )

    run_this >> task


def test_function(**kwargs):
    return 1


task2 = PythonOperator(
        task_id='some_task_id',
        python_callable=test_function,
        op_kwargs={'random_key': 'random_value'},
        dag=dag,
    )

task3 = PythonOperator(
        task_id='some_task_id2',
        python_callable=test_function,
        op_kwargs={'random_key2': 'random_value2'},
        dag=dag,
    )


task2 >> task3

