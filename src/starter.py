import requests
import dev_config as config
from utils import Corpora

class BingBing():
    def __init__(self, query, precision):
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
        for i, r in enumerate(self.results):
            print config.print_str.format(i+1, r['Title'].encode("ascii", "ignore"),
                                             r['Url'],
                                             r["Description"].encode("ascii", "ignore"))
            relevant = raw_input("Is this result relevant? (y/n): ")
            if relevant.strip().lower() == "y":
                self.selectedIDs.append(i)

    def start(self):
        self.results = self.get_results()
        self.print_results()
        self.evaluate()

    def evaluate(self):
        precision = len(self.selectedIDs) / 10.0
        print "Target precision: ", self.precision
        print "Achieved precision: ", precision

        if precision >= self.precision:
            print "Precision achieved. Stopping"
            return
        elif precision == 0:
            print "No documents relevant. Stopping"
            return
        else:
            print "Going for next iteration..."
            self.update_query()

    def update_query(self):
        results = [r["Description"] for r in self.results]
        corpora = Corpora(self.query, results, self.selectedIDs)
        print "Augmenting query..."
        newQueryWords = [word for word, score in corpora.getUpdatedQuery()]
        self.query = " ".join([self.query, newQueryWords[0]])
        print "Restarting search with query: ", self.query
        self.start()

if __name__ == "__main__":
    q = raw_input("Enter Query: ")
    p = float(raw_input("Enter target precision: ").strip())
    if p < 0 or p > 1:
        print "Error: precision should be between 0 and 1"
    else:
        b = BingBing(query=q.strip(), precision=p)
        b.start()
