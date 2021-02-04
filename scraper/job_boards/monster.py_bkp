from bs4 import BeautifulSoup
import sys
import math
from .helpers import HttpHelpers
import re
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
chromeOptions = Options()
# #chromeOptions.headless = True
chromeOptions.add_argument('--headless')
chromeOptions.add_argument('--disable-gpu')

chromeOptions.add_argument('--no-sandbox')
chromeOptions.add_argument('--disable-dev-shm-usage')
PATH = "/usr/bin/chromedriver"
driver = webdriver.Chrome(PATH,chrome_options=chromeOptions)




class MonsterJobs:
    def __init__(self, url):
        self.url = url
        self.helpers = HttpHelpers()
        self.pageRange = 0
        self.totalJobs = 0
    
    def getRange(self):
        page = self.helpers.download_page(self.url)
        if page is None:
            sys.exit('indeed, there was an error downloading indeed jobs webpage. cannot continue further, so fix this first')
        soup = BeautifulSoup(page, 'lxml')
        try:
            count_str = soup.find('h2', class_="figure").get_text()
            max_results = int(count_str.split()[0].replace(',', '').replace('(', ''))
            self.totalJobs = max_results
            max_results = math.ceil(max_results/25)
            self.pageRange = max_results
        except:
            max_results = 0
        return max_results

    def get(self):
        totalPageCount = ((self.pageRange%10) + 1 ) if (self.pageRange > 10 ) else 1
        print("Total " + str(totalPageCount)+ " pages to search for " + str(self.totalJobs) +" jobs.")
        monster_jobs = []
        pageRangeCond = (self.pageRange + 1) if (self.pageRange > 10 ) else 11
        for i in range(10, pageRangeCond):
            pageCount = ((i%10) + 1 ) if (i > 10 ) else 1
            print('Getting jobs from page ' +  str(pageCount))

            driver.get(self.url + '&page=' + str(i))
            driver.set_window_size(1920, 1080)
            #driver.fullscreen_window()
            driver.implicitly_wait(3)
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))).click()
            except:
                pass
              
            jobs = driver.find_element_by_id("SearchResults")
            with open('file.txt', 'w') as file:
                file.write(driver.page_source)
                   
            #page = self.helpers.download_page(self.url + '&page=' + str(i))

            #if page is None:
            #    sys.exit('indeed, there was an error downloading indeed jobs webpage. cannot continue further, so fix this first')

            monster_jobs = monster_jobs + self.__parse_index(jobs)
          

        for job in monster_jobs:
                
            job_content = self.helpers.download_page(job["href"])
            if job_content is None:
                continue

            text, des_element= self.__parse_details(job_content)
            job["description_text"] = text
            job["description"] = des_element
            #job["company_url"] = company_url
    
        return monster_jobs
    
    # def search_tag(self, tag):
    #     return tag.has_attr('data/-jobid') 

    def __parse_index(self, jobs_div):
        
        jobs = jobs_div.find_elements_by_class_name('card-content')
        #jobs = [ div for div in jobs if self.search_tag(div)]
        all_jobs = []
        
        for job in jobs:
            driver.implicitly_wait(2)
            try:
                soup = BeautifulSoup(job.get_attribute('innerHTML'),'html.parser')
                title_elem = soup.find('h2', class_='title')
                company_elem = soup.find('div', class_='company')
                url_elem = soup.find('a')
                job_id = job.get_attribute("data-jobid")
                job_location=soup.find('div',class_='location')
                

                if None in (title_elem, company_elem, url_elem):
                    continue

                href = url_elem.get('href')
                
                #href = "https://job-openings.monster.ca/software-developer-toronto-on-ca-cincinnati-bell-telephone-company-llc/220049250"
                
                if href is None:
                    continue
                
                try:
                    job.click()
                    time.sleep(2)
                    el = driver.find_element_by_id("ContentContainer")
                    #import pdb; pdb.set_trace()
                    soup = BeautifulSoup(el.get_attribute('innerHTML'), 'html.parser')
                    with open('container.txt', 'a') as file:
                        file.write(el.get_attribute('innerHTML'))
                    
                    link = soup.find("a", id="AboutCompanyProfileLink").get('href')
                except:
                    link = ''
                
                item = {

                    "job_id": job_id,
                    "title" : title_elem.text.strip(),
                    "company" : company_elem.text.strip(),
                    "company_url" : link,
                    "href" :href,
                    "location" : job_location.text.strip(),
                    "description" : "",
                    "description_text" : "",
                    "jobtype_keywords" : "",
                    "job_type": "Monster.ca"
                }
                all_jobs.append(item)
            except:
                pass

        
        return all_jobs
        
    def __parse_details(self, htmlcontent):
        soup = BeautifulSoup(htmlcontent, 'lxml')
        description_element = soup.find('div', class_='job-description')
        company_url = soup.find('div', id_='AboutCompany')
        
        try:
            description_text = description_element.text.strip()
            #description_text = re.sub("[^a-zA-Z+3]", " ", description_text)
        except:
                description_text = ""
        # try:
            
        #     company_url = company_url.text.strip()
            
        # except:

        #     company_url = ""

        return (description_text, str(description_element))
        
