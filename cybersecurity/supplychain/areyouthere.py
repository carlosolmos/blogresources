#!/usr/bin/python3

import requests
import time

TOKEN = "__your_token__"

def clean(line):    
    line = line.strip()
    line = line.replace("\"","")
    line = line.replace(",","")
    return line

def getGithubInfo(owner, project):
    global TOKEN
    info={}
    # REPO INFO
    response = requests.get(
        "https://api.github.com/repos/{}/{}".format(owner, project),    
        headers={'Accept': 'application/vnd.github+json',
        'Authorization':"Bearer {}".format(TOKEN),
        'X-GitHub-Api-Version': '2022-11-28'},
    )
    if(response.status_code != 200):
        return None

    json_response = response.json()
    info['url'] = json_response['url']
    info['full_name'] = json_response['full_name']
    info['created_at'] = json_response['created_at']
    info['last_push'] = json_response['pushed_at']
    

    # WEEKLY COMMIT COUNT
    # Returns the total commit counts for the owner and total commit counts in all. all is everyone combined, 
    # including the owner in the last 52 weeks. If you'd like to get the commit counts for non-owners, you can subtract owner from all.
    # The array order is oldest week (index 0) to most recent week.
    response = requests.get(
        "https://api.github.com/repos/{}/{}/stats/participation".format(owner, project),    
        headers={'Accept': 'application/vnd.github+json',
        'Authorization':"Bearer {}".format(TOKEN),
        'X-GitHub-Api-Version': '2022-11-28'},
    )
    if(response.status_code != 200):
        return None

    info['last_year_commit_count'] = 0
    info['last_24_weeks_commit_count'] = 0    
    info['last_12_weeks_commit_count'] = 0
    info['last_4_weeks_commit_count'] = 0    
    
    
    json_response = response.json()
    allContribs = json_response['all']
    
    if allContribs and len(allContribs) == 52:
        for i in range(52):
            week =  allContribs[51-i]
            info['last_year_commit_count'] += week
            if i<24:
                info['last_24_weeks_commit_count'] += week
                if i<12:
                    info['last_12_weeks_commit_count'] += week
                    if i<4:
                        info['last_4_weeks_commit_count'] += week

    """
        Every commit in a year = 1 pts
        Every commit in last 6 months +1pts
        Every commit in last 12 weeks +10pts
        Every commit in the last 4 weeks +100 pts
    """
    info['score'] = (info['last_year_commit_count']) + \
                    (info['last_24_weeks_commit_count']) + \
                    (info['last_12_weeks_commit_count']*10) + \
                    (info['last_4_weeks_commit_count']*100)    


    return info





file1 = open('myproject-deps.json', 'r')
lines = file1.readlines()
count = 0
report={}
print("==GITHUB INFORMATION==")
for line in lines:
    line = clean(line)
    if line.find("github.com") == 0:
        print("{}".format(line))
        toks=line.split("/")
        if len(toks) > 2:
            owner = toks[1]
            project = toks[2]
            key = "github.com/{}/{}".format(owner, project)
            if key not in report:
                info = getGithubInfo(owner, project)
                if info:
                    print(info)
                    report[key]=info['score']
                time.sleep(0.5)

print("\n\n\n")
print("==REPOSITORIES REPORT==")    
for r in report:
    print("{}\t{}".format(r, report[r]))
