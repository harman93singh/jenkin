from django.shortcuts import render, HttpResponse
from .models import *
from .job_boards import indeed, monster
from scraper.models import *
# Create your views here.

def index(request):
    total_jobs = []
    #skill_list = SkillSet.objects.all().values_list('skill_name')
    # print(skill_list)
    job_keywords = ['software+developer','software+tester','software+support','software+intern', 'data+engineer','data+scientist','data+analyst','data+entry','data+science']
    #job_keywords = ['software+developer']
    for keyword in job_keywords:
        indeed_obj = indeed.IndeedJobs('https://ca.indeed.com/jobs?as_and='+ keyword +'&jt=all&l=ontario&fromage=1&limit=50&sort=date&psf=advsrch&from=advancedsearch')
        monster_obj = monster.MonsterJobs('https://www.monster.ca/jobs/search/?q='+ keyword +'&stpage=1&tm=0')
        pageRangeIndeed = indeed_obj.getRange()
        pageRangeMonster = monster_obj.getRange()
        
        print('\nGetting jobs for ' + keyword.replace('+', " ") +' from indeed.ca')
        indeed_jobs = indeed_obj.get()
        print('Getting jobs for ' + keyword.replace('+', " ") +' from monster.ca')
        monster_jobs = monster_obj.get()
        print('Saved job listings for ' + keyword.replace('+', " "))
        total_jobs = total_jobs + monster_jobs + indeed_jobs #+ monster_jobs #+ indeed_jobs 
        
    for job in total_jobs:
         
        #print('Saving job id' + job["job_id"] + ' in database')
        #print('Title: ' + job["title"])
        print('Company: ' + job["company"])
        #print('Url: ' + job["href"])
        #print('job_key' + job["jobtype_keywords"])
        print('job_link' + job["company_url"])
        
        company = Company.objects.get_or_create(name=job["company"])[0]
        if job["job_type"] == "Monster.ca" or job["job_type"] == "monster.ca": 
            company.monster_company_url = job["company_url"]
        else:
            company.indeed_company_url = job["company_url"]
        company.save()
        job_board = JobBoard.objects.get_or_create(name= job["job_type"])[0]
     
        try:
            JobsCanada.objects.create(
                job_id=job["job_id"],
                title=job["title"],
                url=job["href"],
                description=job["description_text"],
                job_types=job["jobtype_keywords"],
                location=job["location"],
                company=company,
                jobBoard= job_board
            )
            print('%s added' % (job["title"],))
        except:
            pass
        
    return HttpResponse("This is inside scraper")
    
