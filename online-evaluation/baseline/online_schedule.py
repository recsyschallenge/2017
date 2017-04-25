'''
Online example

Uses the offline mode to make predictions 
for the online challenge.

by Daniel Kohlsdorf
'''
import time 
import httplib2
import json
from dateutil.parser import parse
import datetime
import parser
from recommendation_worker import *

TMP_ITEMS    = "data/current_items.csv"
TMP_SOLUTION = "data/current_solution.csv"

MODEL        = "data/recsys2017.model" # Model from offline training
USERS_FILE   = "data/users.csv"        # Online user data

TOKEN  = "WElORyB...TgwNmYtMGJiZGYwOTNkZWY2" # your key 
SERVER = "http://recsys.xing.com"

def header(token):
    return {"Authorization" : "Bearer " + token}

def post_url(server):
    return server + "/api/online/submission"

def status_url(server):
    return server + "/api/online/data/status"

def users_url(server):
    return server + "/api/online/data/users"

def items_url(server):
    return server + "/api/online/data/items"

def get_stats():
    http = httplib2.Http()
    content = http.request(status_url(SERVER), method="GET", headers=header(TOKEN))[1].decode("utf-8")
    response = json.loads(content)    
    return parse(response['current']['updated_at'])

def is_ready():
    return get_stats().date() == datetime.date.today()

def download_items():
    http = httplib2.Http()
    content = http.request(items_url(SERVER), method="GET", headers=header(TOKEN))[1].decode("utf-8")
    fp = open(TMP_ITEMS, "w")
    fp.write(content)
    fp.close()
    return parser.select(TMP_ITEMS, lambda x: True, parser.build_item, lambda x: int(x[0]))

def user_info(user_ids):
    return parser.select(
        USERS_FILE, 
        lambda x: int(x[0]) in user_ids and "NULL" not in x,
        parser.build_user, 
        lambda x: int(x[0])
    )

def download_target_users():
    http = httplib2.Http()
    content = http.request(users_url(SERVER), method="GET", headers=header(TOKEN))[1].decode("utf-8") 
    user_ids = set([int(uid) for uid in content.split("\n") if len(uid) > 0])
    return user_info(user_ids)
                  
def process():
    (_, users) = download_target_users()
    (_, items) = download_items()
    target_users = list(users.keys())
    target_items = list(items.keys())
    filename = TMP_SOLUTION
    model = xgb.Booster({'nthread':1})        
    model.load_model(MODEL)
    classify_worker(target_items, target_users, items, users, filename, model)
    
def submit():
    http = httplib2.Http()    
    filename = TMP_SOLUTION
    with open(filename, 'r') as content_file:
        content = content_file.read()
        response = http.request(post_url(SERVER), method="POST", body=content,
            headers=header(TOKEN)
        )[1].decode("utf-8")
        print("SUBMIT: " + filename + " " + response)

if __name__ == "__main__":
    last_submit = None
    while True:
        if is_ready() and last_submit != datetime.date.today():
            process()
            last_submit = datetime.date.today()
            submit()
        else:
            print("Not ready yet: " + str(datetime.date.today()))
        time.sleep(600)
