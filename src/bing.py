"""
Contains all functions relating to getting queries from Bing.
Creating seperate files for different search engines allows for a decoupling 
of the algorithm from the search engine.
"""
import requests

import config
def get_uri(query):
    url = "https://api.datamarket.azure.com/Bing/Search/Web?Query=%27{0}%27&$top=10&$format=json"
    return url.format(query)

def get_results(query, key):
    url = get_uri(query)
    headers = {'Authorization': 'Basic ' + key}
    r = requests.get(url, headers=headers)
    data = r.json()
    return data.get('d').get('results')

if __name__ == '__main__':
	print get_results('Gates')