import sys
sys.path.append("/opt/python")
import json
import boto3
import pandas as pd
from io import StringIO
from datetime import date
from get_data import get_jobs, get_last_page  

def lambda_handler(event, context):
    today = date.today().strftime('%Y%m%d')
    file_name = f"scraped_data/jobs_{today}.csv"

    bucket_name = "jobnet-pipeline"
    s3_client = boto3.client("s3")
    csv_buffer = StringIO()

    last_page = get_last_page()
    jobs = get_jobs(last_page)

    jobs.to_csv(csv_buffer, index=False)

    s3_client.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=csv_buffer.getvalue()
    )

    return {
        "statusCode": 200,
        "body": json.dumps(f"Successfully uploaded {file_name} to {bucket_name}")
    }
