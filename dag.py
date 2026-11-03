"""
Airflow DAG — Deal Performance Analyzer
Runs every Monday at 9am. Generates Claude-powered performance reports
for all deals completed in the previous week and posts to Slack.
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

DAG_ID    = "deal_performance_analyzer"
DAG_OWNER = "demo-owner@demo.com"

default_args = {
    "owner":            DAG_OWNER,
    "retries":          1,
    "retry_delay":      timedelta(minutes=10),
    "email_on_failure": False,
}

with DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    description="Weekly deal performance reports — Claude writes plain-English summaries for business owners",
    schedule="0 9 * * 1",
    start_date=datetime(2024, 8, 1),
    catchup=False,
    tags=["deals", "performance", "claude"],
) as dag:

    def run_reports():
        import os
        os.environ["SLACK_ENABLED"] = "true"
        from performance_analyzer import run_analyzer
        run_analyzer()

    generate_reports = PythonOperator(
        task_id="generate_deal_performance_reports",
        python_callable=run_reports,
    )
