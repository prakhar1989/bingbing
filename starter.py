#!/usr/bin/python

import base64
import requests

# Constants
KEY = "Byygq1zI2KKyssKp8UvVe3DV/v6Aa0FEsKrE+pqDa0s"
ID = "0c3454d3-67ce-4558-b4ac-1e95f964cdf5"
ENCODED = base64.b64encode("{0}:{1}".format(KEY, KEY))

class BingBing():
    def __init__(self, query, precision):
        self.query = query
        self.precision = precision
        self.selectedIDs = []
        self.results = []

    def getURI(self):
        url = "https://api.datamarket.azure.com/Bing/Search/Web?Query=%27{0}%27&$top=10&$format=json"
        return url.format(self.query)

    def getResults(self):
        url = self.getURI()
        headers = {'Authorization': 'Basic ' + ENCODED}
        r = requests.get(url, headers=headers)
        data = r.json()
        return data.get('d').get('results')

    def printResults(self):
        print "-"*50
        for i, r in enumerate(self.results):
            print i, r["Title"], "(" + r["Url"] + ")"
            print " ", r["Description"]
            print "-"*50

    def start(self):
        self.results = self.getResults()
        self.printResults()
        print "Enter which all results are relevant (comma separated):",
        relevant_indices = raw_input()
        self.evaluate(relevant_indices)

    def evaluate(self, response):
        self.selectedIDs = map(lambda x: int(x.strip()), \
                               response.split(','))
        if len(self.selectedIDs)/10.0 >= self.precision: return
        self.updateQuery()

    def updateQuery():
        # fix query and restart start
        print "Continue"


if __name__ == "__main__":
    b = BingBing(query="gates", precision=0.5)
    b.start()
