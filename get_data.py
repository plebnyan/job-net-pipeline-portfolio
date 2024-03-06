import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from tqdm import tqdm


def get_jobs(pages):
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

    for page in tqdm(range(1, pages + 1)):
        url = f"https://www.jobnet.com.mm/jobs-in-myanmar?page={page}"
        link = "https://www.jobnet.com.mm"

        try:
            with requests.get(url) as resp:
                resp.raise_for_status()  # Check for HTTP errors
                content = resp.content
        except requests.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            continue  # Move to the next iteration

        soup = BeautifulSoup(content, "html.parser")
        job_posts = soup.find_all("div", class_="serp-item")

        for job_post in job_posts:
            job_title_element = job_post.find("a", class_="search__job-title ClickTrack-TopList")
            job_link_element = job_post.find("a", class_="search__job-title ClickTrack-TopList")
            company_name_element = job_post.find("p", class_="search__job-subtitle")
            location_element = job_post.find("p", class_="search__job-location").find("span")
            benefit_element = job_post.find("div", class_="search__job-body").find("ul", class_="search__job-list").find("li").find("p", class_="benefit")
            highlight_element = job_post.find("div", class_="search__job-body").find("ul", class_="search__job-list").find_all("li")[-2]
            career_opportunity_element = job_post.find("div", class_="search__job-body").find("ul", class_="search__job-list").find_all("li")[-1]
            job_category_element = job_post.find("div", class_="search__job-footer").find("p", class_="search__job-category").find("span").find("u")
            post_date_element = job_post.find("p", class_="search__job-posted")

            # Check if the elements exist before accessing the text attribute
            job_title = job_title_element.text.strip() if job_title_element else job_post.find("a", class_="search__job-title ClickTrack-JobDetail").text.strip()
            job_link = link + job_link_element.get('href') if job_link_element else link+ job_post.find("a", class_="search__job-title ClickTrack-JobDetail").get("href")
            company_name = company_name_element.text.strip() if company_name_element else "N/A"
            location = location_element.text.strip() if location_element else "N/A"
            benefit = benefit_element.text.strip() if benefit_element else "N/A"
            highlight = highlight_element.text.strip() if highlight_element else "N/A"
            career_opportunity = career_opportunity_element.text.strip() if career_opportunity_element else "N/A"
            job_category = job_category_element.text.strip() if job_category_element else "N/A"
            post_date = post_date_element.text.strip() if post_date_element else "N/A"

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

        # Introduce a delay to avoid potential rate-limiting
        #time.sleep(2)

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
            "page_id":page_ids
        }
    )
    return df


def get_job_details(df):
    headers = ['job_title', 'desc', 'types', 'job_link', 'load_date']
    data = pd.DataFrame(columns=headers)

    links = df['Link'].to_list()

    # Initialize lists outside the loop
    job_titles = []
    j_link = []
    types_desc = []
    types_req = []
    job_desc = []
    job_req = []
    load_date = []

    for url in tqdm(links):
        with requests.get(url) as resp:
            resp.raise_for_status()
            content = resp.content

        soup = BeautifulSoup(content, "html.parser")

        title_element = soup.find("p", class_="job-details__card-title")
        title = title_element.get_text() if title_element else "N/A"
        job_titles.append(title)

        jd_element = soup.find("div", class_='job-details__description-wrapper job-details__description-wrapper-1')
        jd = [li.text.strip() for li in jd_element.find_all('li')] if jd_element else ["N/A"]
        job_desc.extend(jd)

        requirement_element = soup.find("div", class_='job-details__description-wrapper job-details__description-wrapper-3')
        requirement = [li.text.strip() for li in requirement_element.find_all('li')] if requirement_element else ["N/A"]
        job_req.extend(requirement)

        types_desc.extend(["Job Descriptions"] * len(jd))
        types_req.extend(["Requirements"] * len(requirement))

        j_link.extend([url] * len(jd))
        load_date.extend([datetime.now()] * len(jd))

    new_df = pd.DataFrame({
        'job_title': job_titles,
        'desc': job_desc,
        'types': types_desc + types_req,
        'job_link': j_link,
        'load_date': load_date
    })

    rd = pd.concat([data, new_df], ignore_index=True)
    return rd