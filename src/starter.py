import requests
import config
import sys
from corpora import Corpora

# Hack for turning off SSLWarning on CLIC machines :|
requests.packages.urllib3.disable_warnings()

class BingBing():
    def __init__(self, query, precision, key):
        self.query = query
        self.precision = precision
        self.selectedIDs = []
        self.results = []
        self.KEY = key.strip() or config.ENCODED_KEY

    def get_uri(self):
        url = "https://api.datamarket.azure.com/Bing/Search/Web?Query=%27{0}%27&$top=10&$format=json"
        return url.format(self.query)

    def get_results(self):
        url = self.get_uri()
        headers = {'Authorization': 'Basic ' + self.KEY}
        r = requests.get(url, headers=headers)
        data = r.json()
        return data.get('d').get('results')

    def print_results(self):
        for i, r in enumerate(self.results):
            print config.print_str.format(i+1, r['Title'].encode("ascii", "ignore"),
                                             r['Url'],
                                             r["Description"].encode("ascii", "ignore"))
            try: # graceful exits on <C-d> / <C-c>
                relevant = raw_input("Is this result relevant? (y/n): ").strip().lower()
                while relevant not in "yn":
                    relevant = raw_input("Please enter only y (for yes) or n (for no): ").strip().lower()
                if relevant == "y":
                    self.selectedIDs.append(i)
            except (EOFError, KeyboardInterrupt) as e:
                print "\nExiting..."
                sys.exit()

    def start(self):
        self.results = self.get_results()
        self.selectedIDs = []
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
        results = [r["Description"] + r['Title'] for r in self.results]
        corpora = Corpora(self.query, results, self.selectedIDs)
        print "Augmenting query..."
        updatedQuery = corpora.getUpdatedQuery()
        print updatedQuery
        newQueryWords = [word for word, score in updatedQuery if score > 2]
        return
        self.query = " ".join([self.query] +  newQueryWords)
        print "Restarting search with query: ", self.query
        self.start()

if __name__ == "__main__":
    try: # graceful exits on <C-d> / <C-c>
        q = raw_input("Enter Query: ")
        p = float(raw_input("Enter target precision: ").strip())
        key = raw_input("Enter BING account key (leave blank to use author's key): ")
    except (EOFError, KeyboardInterrupt) as e:
        print "\nExiting..."
        sys.exit()
    if p < 0 or p > 1:
        print "Error: precision should be between 0 and 1. Please try again."
        sys.exit()

    b = BingBing(query=q.strip(), precision=p, key=key)
    b.start()
