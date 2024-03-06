import pandas as pd


df = pd.read_csv('scraping/scraped_data/jobs_20240228.csv')
df.to_csv('scraping/scraped_data/test.csv')