import sys
sys.path.insert(0, '..')
from parse_to_mongo.parse_jobs_to_mongo import load_jobs_to_mongo
from parse_to_mongo.filter_on_salary import filter_on_salary

# load data to mongo collection
load_jobs_to_mongo()

# filter jobs by salary and return pandas DataFrame
d = filter_on_salary(threshold=100000, bounds='min')