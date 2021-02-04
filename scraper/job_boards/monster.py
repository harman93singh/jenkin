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
from nltk.corpus import stopwords
chromeOptions = Options()
chromeOptions.headless = True
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
            #with open('file.txt', 'w') as file:
            #    file.write(driver.page_source)
                   
            monster_jobs = monster_jobs + self.__parse_index(jobs)
          

        for job in monster_jobs:
            job_content = self.helpers.download_page(job["href"])
            if job_content is None:
                continue
            text, des_element,job_type= self.__parse_details(job_content)
            job["description_text"] = text
            job["description"] = des_element
            job["jobtype_keywords"] = job_type
    
        return monster_jobs
    
    def __parse_index(self, jobs_div):
        
        jobs = jobs_div.find_elements_by_class_name('card-content')
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
                if href is None:
                    continue
                
                try:
                    job.click()
                    time.sleep(2)
                    el = driver.find_element_by_id("ContentContainer")
                    soup = BeautifulSoup(el.get_attribute('innerHTML'), 'html.parser')
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
        except:
                description_text = ""
        try:
            job_type_k = self.keywords_extract(description_text)
        except:
            job_type_k = ""
        return (description_text, str(description_element),job_type_k)
    
    
    def keywords_extract(self,text):
        jobtype_dict = ['full-time', 'part-time','contract','permanent', 'remote' ,'temporarily remote','co-op' ,'internship','freelance','contract']
        text = re.sub("[^a-zA-Z+3]", " ", str(text))
        text = text.lower().split()
        stops = set(stopwords.words("english"))  
        text = [w for w in text if not w in stops]
        text = list(set(text))
        jobtype_keyword = [str(word) for word in text if word in jobtype_dict ]
        return jobtype_keyword    
