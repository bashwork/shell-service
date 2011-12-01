#!/usr/bin/env python
import httplib2
from random import randint, uniform

def generate_data(id, day):
    date = "&date=2010-10-%02d 12:12:12" % day
    format = "player=%d&hits=%d&temperature=%.2f&humidity=%.2f&acceleration=%.2f&status=%d" + date
    return format % (id, randint(0,100), uniform(97, 102), uniform(0, 100), uniform(10, 100), randint(0,3))

def post_request(data):
    print data
    client = httplib2.Http(".cache")
    #host = "http://localhost:8000/api/v1/history/"
    host = "http://radiant-meadow-2958.herokuapp.com/api/v1/history/"
    response, content = client.request(host, "POST", body=data,
        headers = {'content-type':'application/x-www-form-urlencoded'})
    if response.status != 200: print content

def create_player_history(id, count):
    for day in range(1, count):
        data = generate_data(id,day)
        post_request(data)

for player in range(1,12):
    create_player_history(player, 20)
