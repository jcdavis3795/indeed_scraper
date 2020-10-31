from bs4 import BeautifulSoup
import requests
import sys
from datetime import date
import csv



# initialize storage
company = []
title = []
desc = []
link = []

date = date.today()
today = str(date)

source = requests.get('https://www.indeed.com/jobs?q=python%20developer&l=Dallas%2C%20TX&radius=50&explvl=entry_level&start=0&limit=50').text

soup = BeautifulSoup(source, 'html.parser')

# initialize index
index = 0

# unique filename based on date searched
sys.stdout = open(today+'.csv', 'w')
csv_writer = csv.writer(sys.stdout)
csv_writer.writerow(['COMPANY','JOB TITLE','DESCRIPTION', 'LINK'])

for job in soup.find_all('div', class_='jobsearch-SerpJobCard unifiedRow row result'):

    link_id = job['data-jk']

    company_name = job.div.span
    job_title = job.h2.a
    job_desc = job.ul.li
    job_page_link = (f'https://www.indeed.com/jobs?q=python%20developer&l=Dallas%2C%20TX&radius=50&explvl=entry_level&start=0&limit=50&vjk={link_id}')

    # if information is not in the right location
    if None in (company_name, job_title, job_desc, job_page_link):
        continue

    company.append(company_name.text.strip())
    title.append(job_title.text.strip())
    desc.append(job_desc.text.strip())
    link.append(job_page_link)

    csv_writer.writerow([company[index], title[index], desc[index],link[index]])

    # print(index, ' ', company_name.text, job_title.text, ':', '\n', job_desc.text, '\n', job_page_link)

    index += 1

# second page of job search
source_2 = requests.get('https://www.indeed.com/jobs?q=python%20developer&l=Dallas%2C%20TX&radius=50&explvl=entry_level&start=51&limit=50').text

soup_2 = BeautifulSoup(source_2, 'html.parser')

for job in soup_2.find_all('div', class_='jobsearch-SerpJobCard unifiedRow row result'):

    link_id_2 = job['data-jk']

    company_name_2 = job.div.span
    job_title_2 = job.h2.a
    job_desc_2 = job.ul.li
    job_page_link_2 = (f'https://www.indeed.com/jobs?q=python%20developer&l=Dallas%2C%20TX&radius=50&explvl=entry_level&start=51&limit=50&vjk={link_id_2}')

    if None in (company_name_2, job_title_2, job_desc_2, job_page_link_2):
        continue

    company.append(company_name_2.text.strip())
    title.append(job_title_2.text.strip())
    desc.append(job_desc_2.text.strip())
    link.append(job_page_link_2)

    csv_writer.writerow([company[index], title[index], desc[index], link[index]])

    # print(index, ' ', company_name_2.text, job_title_2.text, ':', '\n', job_desc_2.text, '\n', job_page_link_2)

    index += 1

sys.stdout.close()
