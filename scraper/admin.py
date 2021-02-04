from django.contrib import admin
from scraper.models import Company
from scraper.models import JobBoard
from scraper.models import JobsCanada
from scraper.models import SkillType
from scraper.models import SkillSet


admin.site.register(Company)
admin.site.register(JobBoard)
admin.site.register(JobsCanada)
admin.site.register(SkillType)
admin.site.register(SkillSet)