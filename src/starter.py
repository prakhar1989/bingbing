import requests
import dev_config as config
from utils import Corpora

class BingBing():
    def __init__(self, query, precision):
        """
        :param query: the query string
        :param precision: the requisite accuracy.
        """
        self.query = query
        self.precision = precision
        self.selectedIDs = []
        self.results = []

    def get_uri(self):
        url = "https://api.datamarket.azure.com/Bing/Search/Web?Query=%27{0}%27&$top=10&$format=json"
        return url.format(self.query)

    def get_results(self):
        url = self.get_uri()
        headers = {'Authorization': 'Basic ' + config.ENCODED_KEY}
        r = requests.get(url, headers=headers)
        data = r.json()
        return data.get('d').get('results')

    def print_results(self):
        print "-" * 50
        for i, r in enumerate(self.results):
            print config.print_str.format(i, r['Title'], r['Url'],
                                          r["Description"].encode('ascii', 'ignore'))

    def start(self):
        self.results = self.get_results()
        self.print_results()
        print "Enter which all results are relevant (comma separated):",
        relevant_indices = raw_input()
        self.evaluate(relevant_indices)

    def evaluate(self, response):
        self.selectedIDs = map(lambda x: int(x.strip()),
                               response.split(','))
        if len(self.selectedIDs) / 10.0 >= self.precision: return
        self.update_query()

    def update_query(self):
        results = [r["Description"] for r in self.results]
        corpora = Corpora(self.query, results, self.selectedIDs)
        corpora.getUpdatedQuery()

if __name__ == "__main__":
    query = raw_input("Enter Query: ")
    b = BingBing(query=query.strip(), precision=0.5)
    b.start()
