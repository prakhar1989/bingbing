#!/usr/bin/python

import requests

import dev_config as config
# Constants

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
        headers = {'Authorization': 'Basic ' + config.ENCODED_KEY}
        r = requests.get(url, headers=headers)
        data = r.json()
        return data.get('d').get('results')

    def printResults(self):
        print "-"*50
        for i, r in enumerate(self.results):
            # print i, r["Title"], "(" + r["Url"] + ")"
            # print " ", r["Description"].encode('ascii','ignore')
            # print "-"*50
            print config.print_str.format(i, r['Title'], r['Url'], r["Description"].encode('ascii','ignore'))
    def start(self):
        self.results = self.getResults()
        self.printResults()
        print "Enter which all results are relevant (comma separated):",
        relevant_indices = raw_input()
        self.evaluate(relevant_indices)

    @staticmethod
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
