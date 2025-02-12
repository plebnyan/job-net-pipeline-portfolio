import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date

today = date.today()

def get_last_page():
    
    url = "https://www.jobnet.com.mm/jobs-in-myanmar?page=10000"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")
    last_page_element = soup.find("span", class_="search__action-btn active")
    last_page = int(last_page_element.text.strip())
    return last_page



def get_jobs(last_page):

    job_titles = []
    company_names = []
    locations = []
    benefits = []
    highlights = []
    career_opportunities = []
    job_categories = []
    job_links = []
    post_dates = []
    page_ids = []
    
    base_url = "https://www.jobnet.com.mm"
    
    for page in range(1,last_page):
    #while True:
        url = f"{base_url}/jobs-in-myanmar?page={page}"

        
        resp = requests.get(url)
        resp.raise_for_status()
        content = resp.content
        

        soup = BeautifulSoup(content, "html.parser")
        job_posts = soup.find_all("div", class_="serp-item")

        if not job_posts:
            print(f"No job listings found on page {page}. Stopping.")
            break  # Stop if no jobs found

        for job_post in job_posts:
            job_title_element = job_post.find("a", class_="search__job-title ClickTrack-TopList")
            job_title_element2 = job_post.find("a", class_="search__job-title ClickTrack-JobDetail") 
            job_link_element = job_post.find("a", class_="search__job-title ClickTrack-TopList")
            job_link_element2 = job_post.find("a", class_="search__job-title ClickTrack-JobDetail")
            company_name_element = job_post.find("p", class_="search__job-subtitle")
            location_element = job_post.find("p", class_="search__job-location")
            post_date_element = job_post.find("p", class_="search__job-posted")

            # Check if elements exist before extracting text
            job_title = job_title_element.text.strip() if job_title_element else job_title_element2.text.strip()
            job_link = base_url + job_link_element.get("href") if job_link_element else base_url + job_link_element2.get("href")
            company_name = company_name_element.text.strip() if company_name_element else "N/A"
            location = location_element.find("span").text.strip() if location_element and location_element.find("span") else "N/A"
            post_date = post_date_element.text.strip() if post_date_element else "N/A"

            # Extract additional details safely
            benefit_element = job_post.select_one(".search__job-body ul.search__job-list li p.benefit")
            highlight_elements = job_post.select(".search__job-body ul.search__job-list li")
            job_category_element = job_post.select_one(".search__job-footer p.search__job-category u")

            benefit = benefit_element.text.strip() if benefit_element else "N/A"
            highlight = highlight_elements[-2].text.strip() if len(highlight_elements) > 1 else "N/A"
            career_opportunity = highlight_elements[-1].text.strip() if highlight_elements else "N/A"
            job_category = job_category_element.text.strip() if job_category_element else "N/A"

            # Append to lists
            job_titles.append(job_title)
            company_names.append(company_name)
            locations.append(location)
            benefits.append(benefit)
            highlights.append(highlight)
            career_opportunities.append(career_opportunity)
            job_categories.append(job_category)
            job_links.append(job_link)
            post_dates.append(post_date)
            page_ids.append(page)

    # Create DataFrame
    df = pd.DataFrame(
        {
            "Titles": job_titles,
            "Company": company_names,
            "Category": job_categories,
            "Location": locations,
            "Benefits": benefits,
            "Highlights": highlights,
            "Opportunities": career_opportunities,
            "Posted_Date": post_dates,
            "Link": job_links,
            "page_id": page_ids
        }
    )
    return df


def get_job_details(df):

        headers = ['job_title','desc','types','job_link','load_date']
        data=pd.DataFrame(columns=headers)

        job_titles=[]
        j_link=[]
        types_desc=[]
        types_req=[]
        job_desc=[]
        job_req=[]
        load_date=[]
    
        links= df['Link'].to_list()
        #links=["https://www.jobnet.com.mm/job/project-manager-pmo-hana-microfinance-ltd/94611"]
        for url in tqdm(links[:3]):
            with requests.get(url) as resp:
                resp.raise_for_status()  
                content = resp.content

            job_titles=[]
            j_link=[]
            types_desc=[]
            types_req=[]
            job_desc=[]
            job_req=[]
            load_date=[]
            soup = BeautifulSoup(content, "html.parser")


            title_element = soup.find("p", class_="job-details__card-title")
            title = title_element.get_text() if title_element else "N/A"
            job_titles.append(title)

            jd_element = soup.find("div", class_='job-details__description-wrapper job-details__description-wrapper-1')
            jd = [li.text.strip() for li in jd_element.find_all('li')] if jd_element else ["N/A"]
            for i in jd:
                job_desc.append(i)

            requirement_element = soup.find("div", class_='job-details__description-wrapper job-details__description-wrapper-3')
            requirement = [li.text.strip() for li in requirement_element.find_all('li')] if requirement_element else ["N/A"]

            for r in requirement:
                job_req.append(r)

            
            types_desc.append('Job Descriptions')
            td=types_desc*len(jd)
            
            
            types_req.append("Requirements")
            tr=types_req*len(requirement)
            
            
            types=td+tr
            
            job_desc.extend(job_req)

            jt=job_titles*len(job_desc)

            j_link.append(url)
            lin=j_link*len(job_desc)

            load_date.append(datetime.now())
            ld=load_date*len(job_desc)

        new_df= pd.DataFrame({
                'job_title':jt,
                'desc':job_desc,
                'types':types,
                'job_link':lin,
                'load_date':ld
            })
            
        
        return pd.concat([data,new_df],ignore_index=True)
