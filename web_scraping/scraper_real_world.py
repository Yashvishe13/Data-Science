from typing import Text
from bs4 import BeautifulSoup
import pandas as pd
import  requests

dataset = pd.DataFrame(columns=['Name', 'skills', 'more_info'])

unfamiliar_skill = input('Enter unfamiliar skill: ')
print(f'Filtering out {unfamiliar_skill}')
print(f'Fetching output...')    

html_text = requests.get("https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=").text
soup = BeautifulSoup(html_text, 'lxml')
jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
for job in jobs:
    published_date = job.find('span', class_='sim-posted').span.text
    if 'few' in published_date:
        company_name = job.find('h3', class_='joblist-comp-name').text.replace(' ', '').strip()
        skills = job.find('span', class_='srp-skills').text.replace(' ', '').strip()
        if unfamiliar_skill not in skills:
            more_info = job.header.h2.a['href']
            
            dataset = dataset.append({'Name': company_name, 'skills': skills, 'more_info': more_info}, ignore_index=True)
            
dataset.to_csv('jobs_info.csv')