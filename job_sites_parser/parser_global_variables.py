import sys
sys.path.insert(0, '..')

import datetime
from dotenv import load_dotenv
import os


TAGS_HH = ['id', 'alternate_url','name','address', 'published_at', 'description',
        'employer', 'employment', 'experience', 'salary', 'type', 'key_skills',
        'site', 'specializations', 'archived']

TAGS_SUPERJOB = ['id', 'link', 'profession', 'address', 'date_published', 
                 'vacancyRichText','firm_name', 'type_of_work','experience', 
                 'payment_from', 'payment_to', 'is_closed', 'candidat',
                 'catalogues', 'is_archive']

HH_URL = 'https://api.hh.ru/vacancies'
superjob_api_version = 2.33
SUPERJOB_URL = f'https://api.superjob.ru/{superjob_api_version}/vacancies'

HH_AREA = '113' # Russia
SUPERJOB_AREA = 1 # Russia

DATE_FROM = datetime.date.today() - datetime.timedelta(days = 30*6)
DATE_TO = datetime.date.today()

PER_PAGE = '100'


load_dotenv()
SUPERJOB_SECRET = os.getenv("SUPERJOB_SECRET")
