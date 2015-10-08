import requests
import sys

import config
from corpora import Corpora
import bing

# Hack for turning off SSLWarning on CLIC machines :|
requests.packages.urllib3.disable_warnings()

class BingBing():
    def __init__(self, query, precision, key):
        self.query = query
        self.precision = precision
        self.selectedIDs = []
        self.results = []
        self.KEY = key.strip() or config.ENCODED_KEY

    def get_results(self):
        return bing.get_results(self.query, self.KEY)


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
        try:
            corpora = Corpora(self.query, results, self.selectedIDs)
            print corpora
        except:
            print "NLTK Corpora not install, query expansion requires NLKT Corpuses"
        print "Augmenting query..."

        # filter - choose words that are not in the query already
        candidates = [(w, s) for w, s in corpora.getUpdatedQuery() \
                      if w not in set(self.query.split())]
        (w1, s1), (w2, s2) = candidates[0], candidates[1]
        newQueryWords = [w1, w2] if s1 == s2 else [w1]

        # build new query
        self.query = " ".join([self.query] +  newQueryWords)
        print "Restarting search with query: ", self.query
        self.start()

if __name__ == "__main__":
    try: # graceful exits on <C-d> / <C-c>
        q = raw_input("Enter Query: ")
        p = 0
        while p <= 0 or p > 1:
            p = float(raw_input("Enter target precision (Prescision needs to be between 0 and 1): ").strip())
        key = raw_input("Enter BING account key (leave blank to use author's key): ")
    except (EOFError, KeyboardInterrupt) as e:
        print "\nExiting..."
        sys.exit()

    b = BingBing(query=q.strip(), precision=p, key=key)
    b.start()
