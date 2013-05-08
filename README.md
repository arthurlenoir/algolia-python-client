Algolia Python Client 
=====================
http://www.algolia.com/features/

About
-----
pyAlgolia is a python client for Algolia Search Cloud. 

Installation
------------
python setup.py install

Examples
--------
```python
>>> from pyalgolia import Client

>>> # Init the client
>>> algolia = Client(host='api.algolia.com', app_id='your_app_id', api_key='your_api_key')

>>> # Add contacts
>>> algolia.add('contact', 1, {'last_name': "Obama", 'first_name': "Barack"})
{u'objectID': u'1', u'taskID': 99171, u'updatedAt': u'2013-05-08T11:18:48.926Z'}

>>> algolia.add('contact', 2, {'last_name': "Clinton", 'first_name': "Bill"})
{u'objectID': u'2', u'taskID': 99180, u'updatedAt': u'2013-05-08T11:19:09.419Z'}

>>> # Search
>>> algolia.search('contact', query='B')
{u'hits': [{u'first_name': u'Barack', u'last_name': u'Obama', u'_highlightResult': {u'first_name': {u'matchLevel': u'full', u'value': u'<em>B</em>arack'}, u'last_name': {u'matchLevel': u'none', u'value': u'Obama'}}, u'objectID': u'1'}, {u'first_name': u'Bill', u'last_name': u'Clinton', u'_highlightResult': {u'first_name': {u'matchLevel': u'full', u'value': u'<em>B</em>ill'}, u'last_name': {u'matchLevel': u'none', u'value': u'Clinton'}}, u'objectID': u'2'}], u'processingTimeMS': 1, u'nbHits': 2, u'hitsPerPage': 20, u'params': u'query=B', u'nbPages': 1, u'query': u'B', u'page': 0}


>>> algolia.search('contact', query='Bi')
{u'hits': [{u'first_name': u'Bill', u'last_name': u'Clinton', u'_highlightResult': {u'first_name': {u'matchLevel': u'full', u'value': u'<em>Bi</em>ll'}, u'last_name': {u'matchLevel': u'none', u'value': u'Clinton'}}, u'objectID': u'2'}], u'processingTimeMS': 1, u'nbHits': 1, u'hitsPerPage': 20, u'params': u'query=Bi', u'nbPages': 1, u'query': u'Bi', u'page': 0}
```

API Specification
-----------------
http://docs.algoliav1.apiary.io/