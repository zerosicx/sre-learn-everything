from typing import List
from bs4 import BeautifulSoup
import requests
import json
import os
from dotenv import load_dotenv
from convex import ConvexClient

load_dotenv(".env.local")
load_dotenv()
client = ConvexClient(os.getenv("CONVEX_URL"))


# ************************ SCHEMA ************************

class Job:
    # Populate with input and default values
    def __init__(self, job_title, location, date):
        self.job_title = job_title
        self.location = location
        self.date = date
        self.seen = False
        
# ************************ FUNCTIONALITY ************************

software_jobs_prosple = "https://nz.prosple.com/search-jobs?keywords=software+intern&locations=796&defaults_applied=1"
jobs: List[Job] = []


def scrape_jobs():
    page_to_scrape = requests.get(software_jobs_prosple)
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")
    job_titles = soup.findAll('h2', attrs={'class':'sc-eCssSg kgSmcY heading sc-hjWSAi gjFcJS'});
    locations = soup.findAll('p', {'class':'sc-kiYtDG hHYCJM'})
    dates = soup.findAll('div', {'class':'sc-cbDGPM eTEuVf field-item'})

    for i in range(0, len(job_titles)):
        # Extract values or set them to None if they are null
        title = job_titles[i].text if i < len(job_titles) else None
        loc = locations[i].text if i < len(locations) else None
        date = dates[i].text if i < len(dates) else None
        
        # Create a new job object and add it to the list of jobs
        j = Job(title, loc, date)
        jobs.append(j)

# Used for checking what type of jobs were scraped
# def display_jobs():
#     json_data = [job.__dict__ for job in jobs]
#     json_string = json.dumps(json_data, indent=4)
    
def upload_jobs():
    # make a query to convex
    for job in jobs:
        job_dict = job.__dict__
        # Check if the job already exists by querying Convex
        existing_job = client.query("jobs:getByTitle", {"jobTitle": job_dict['job_title']})
        
        # If the job doesn't already exist, create it
        if not existing_job:
            # Create the job
            create_job_args = {
                "jobTitle": job_dict['job_title'],
                "location": job_dict['location'],
                "date": job_dict['date'],
                "seen": False  # Assuming 'seen' should be set to False when creating a new job
            }
            client.mutation("jobs:createJob", create_job_args)
            print(f"Job '{job_dict['job_title']}' created successfully.")
        else:
            print(f"Job '{job_dict['job_title']}' already exists. Skipping...")
            
            
def display_existing_jobs():
    jobs = client.query("jobs:get");
    json_string = json.dumps(jobs, indent=4)
    print(json_string)

if __name__ == "__main__":
    # scrape_jobs()
    # upload_jobs()
    display_existing_jobs()