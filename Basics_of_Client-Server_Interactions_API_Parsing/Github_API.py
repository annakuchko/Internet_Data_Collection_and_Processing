# 1. Посмотреть документацию к API GitHub, разобраться как вывести
# список репозиториев для конкретного пользователя, сохранить 
# JSON-вывод в файле *.json.

# import libraries
import requests
from pprint import pprint as pp
import json

# username = input("Enter the username:")
username = 'annakuchko'

# get user repos using GitHub REST API
try:
    r = requests.get(f'https://api.github.com/users/{username}/repos')
    repos_json = r.json()
    repos_dict = {}
    # create dictionary of repos names and urls
    for i in range(0, len(repos_json)):
        repos_dict[repos_json[i]["name"]] = repos_json[i]['svn_url']
    
    # print dictionary of repos names and urls
    pp(repos_dict)
    
    #save repos_json to file
    if r.ok:
        path = f"{username}_repos.json"
        with open(path, "w") as f:
            json.dump(repos_json, f, indent=2)
    else:
        pp(r.status_code)

except:
    raise Exception(f'Status code: {r.status_code}')
