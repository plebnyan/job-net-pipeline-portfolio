import requests
from bs4 import BeautifulSoup
import pandas as pd
from get_data import get_jobs,get_job_details






 
 
df = pd.read_csv('jobs.csv')
#df.to_csv('jobs.csv')
jd=get_job_details(df)
jd.to_csv('job_details.csv',index=False)
