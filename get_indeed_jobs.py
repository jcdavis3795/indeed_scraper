from bs4 import BeautifulSoup
import requests
import math

# the first thing i did here was get the html text of the first page of my indeed search. I found where on the page the total number of jobs was listed, and
#using that number, found the total number of pages to scrape through. There's probably a better way to do that, but this was my solution
source = requests.get('https://www.indeed.com/jobs?q=python%20developer&l=Dallas%2C%20TX&radius=50&explvl=entry_level&'
                      'limit=50&start=0').text

soup = BeautifulSoup(source, 'lxml')

page_count = soup.find(id='searchCountPages').text

num_jobs = page_count.split(' ')[23]

# each page displays 50 results. Dividing the number of jobs by 50 and then rounding up gives us the total number of pages to scrape through
num_pages_int = (int(num_jobs)/50)
num_pages = math.ceil(num_pages_int)


def get_jobs(web_page_num):

    from datetime import date
    import sys
    import csv

    indeed_links = []

    page_num = 1

    date = date.today()
    today = str(date)

    # unique filename based on date searched
    sys.stdout = open(today + '.csv', 'w')
    csv_writer = csv.writer(sys.stdout)
    csv_writer.writerow(['COMPANY', 'JOB TITLE', 'DESCRIPTION', 'LINK'])

    for pages in range(web_page_num):

        links = f'https://www.indeed.com/jobs?q=python%20developer&l=Dallas%2C%20TX&radius=50&explvl=entry_level&' \
                f'limit=50&start={page_num}'
        links_source = requests.get(links).text
        indeed_links.append(links)

        page_num += 50

        company = []
        title = []
        desc = []
        link = []

        indeed_soup = BeautifulSoup(links_source, 'html.parser')

        index = 0

        for job in indeed_soup.find_all('div', class_='jobsearch-SerpJobCard unifiedRow row result'):

            link_id = job['data-jk']

            company_name = job.div.span
            job_title = job.h2.a
            job_desc = job.ul.li
            job_page_link = (f'https://www.indeed.com/jobs?q=python%20developer&l=Dallas%2C%20TX&radius=50&explvl='
                             f'entry_level&start=0&limit=50&vjk={link_id}')

            # if information is not in the right location
            if None in (company_name, job_title, job_desc, job_page_link):
                continue

            company.append(company_name.text.strip())
            title.append(job_title.text.strip())
            desc.append(job_desc.text.strip())
            link.append(job_page_link)

            csv_writer.writerow([company[index], title[index], desc[index], link[index]])

            index += 1

    sys.stdout.close()


get_jobs(num_pages)

