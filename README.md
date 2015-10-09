Bingbing
===

### Team Members (in alphabetical order)
- Nikhil Mitra (nm2868)
- Prakhar Srivastav (ps2894)

### File List
```
├── README.md
├── outputs
│   ├── musk-output.txt
│   ├── gates-output.txt
│   └── taj-mahal-output.txt
├── requirements.txt
├── run.sh
├── src
│   ├── __init__.py
│   ├── corpora.py
│   ├── dev_config.py
│   └── starter.py
└── tests
    ├── __init__.py
    └── corpora_test.py
```

### Run

In order to run the code, just install the python packages the program depends on. A list of these packges is provided in the the `requirements.txt` file.

```
$ pip install -r requirements.txt
$ ./run.sh
```

### Bing Account Key
The bing account key is `Byygq1zI2KKyssKp8UvVe3DV/v6Aa0FEsKrE+pqDa0s`

### Internal Design
The algorithm used is **Rocchio's Algorithm**[1]. It is implemented in corpora.py, along with a implementation of the linear TF/IDF. All configurable settings are present in config.py

####Folder Structure
The folder *outputs* contains sample outputs of the algorithm.<br>
The folder *src* contains the main source code.
The folder "tests" contains basic test cases.

### TODO:

 1. Change from TF/IDF to TextRank[2] or RAKE[3]. Both these algorithms provide superior accuracy and do not rely on the size of the document corpus [4]
 2. Write automatic test cases.
 3. Ab-Initio starting with Bing. Bing has some form of query expansion running underneath, and repeated searching tends to alter search results.
 3. Implement more search engines. 
 4. Implement a document clustering algorithm to account for false negative or a false positive given during feedback.
 5. Implement term correlation using N degrees of Wikipedia, DMOZ categorizer or WordNet. From experience, DMOZ works best (and fast) [5]

----------


[1] Relevance Feedback in Information Retrieval, SMART Retrieval System Experiments in Automatic Document Processing, 1971, Prentice Hall Inc.

[2] Rada Mihalcea and Paul Tarau, “TextRank: Bringing order into texts”, Association for Computational Linguistics, 2004.

[3] Martin Dostál and Karel Jezek, “Automatic Keyphrase Extraction based on NLP and Statistical Methods”, DATESO, pp. 140-145, 2011.

[4] Stuart Rose, Dave Engel, Nick Cramer and Wendy Cowley, “Automatic keyword extraction from individual documents”, Text Mining: Applications and Theory, pp. 1- 20, 2010.

[5] Mitra, Nikhil, et al. "Adaptive Content Based Textual Information Source Prioritization" ICTACT Journal on Soft Computing 5.1 (2014).