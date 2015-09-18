#!/usr/bin/python

import base64
import requests

KEY = "Byygq1zI2KKyssKp8UvVe3DV/v6Aa0FEsKrE+pqDa0s"
ID = "0c3454d3-67ce-4558-b4ac-1e95f964cdf5"

encoded = base64.b64encode("{0}:{1}".format(KEY, KEY))
headers = {'Authorization': 'Basic ' + encoded}

def getURIFromQuery(query):
    url = "https://api.datamarket.azure.com/Bing/Search/Web?Query=%27{0}%27&$top=10&$format=json"
    return url.format(query)


def getResults(query):
    url = getURIFromQuery(query)
    r = requests.get(url, headers=headers)
    return r.json()

def printResults(results):
    print "-"*50
    for i, r in enumerate(results):
        print i, r["Title"], "(" + r["Url"] + ")"
        print " ", r["Description"]
        print "-"*50

def begin(query):
    results = getResults(query)["d"]["results"]
    printResults(results)
    print "Enter which all results are relevant (comma separated):",
    relevant_indices = raw_input()

if __name__ == "__main__":
    begin("gates")
