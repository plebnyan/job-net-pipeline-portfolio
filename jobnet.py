import requests
from bs4 import BeautifulSoup
import pandas as pd
from get_data import get_jobs,get_job_details
import datetime

to_day = datetime.datetime.now().strftime("%Y%m%d")


file_name = f"jobs_{to_day}.csv"


jobs = get_jobs(65)
jobs.to_csv(file_name,index=False)
