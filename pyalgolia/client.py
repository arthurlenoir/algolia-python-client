import json
import urllib
from httplib import HTTPSConnection

class Client:
    def __init__(self, host, app_id, api_key, batch_size=1000):
        self.host = host
        self.app_id = app_id
        self.api_key = api_key
        self.batch_size = batch_size
        self.requests = {}
        self.headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'X-Algolia-API-Key': self.api_key,
            'X-Algolia-Application-Id': self.app_id,
        }
        self.connection = HTTPSConnection(self.host)

    def execute_request(self, request, method='GET', body=None, retry=0):
        if retry < 3:
            try:
                self.connection.request(method, request, body, self.headers)
                response = self.connection.getresponse().read()
            except Exception, e:
                self.connection = HTTPSConnection(self.host)
                return self.execute_request(request, method, body, retry+1)
            return json.loads(response)
        return { "message": "An unexpected error occured" }

    def start_batch(self, index_name):
        if index_name not in self.requests:
            self.requests[index_name] = []

    def end_batch(self, index_name):
        response = None
        if index_name in self.requests:
            requests = self.requests[index_name]
            if len(requests) > 0:
                data = json.dumps({'requests': requests})
                response = self.execute_request("/1/indexes/%s/batch" % index_name, 'POST', data)
            del self.requests[index_name]
        return response

    # Lists your indexes. Returns also a pendingTask flag per index that indicates if it has remaining task(s) running.
    def get_index(self, index_name):
        return self.execute_request("/1/indexes/%s" % index_name, 'GET')

    # delete an existing index
    def delete_index(self, index_name):
        return self.execute_request("/1/indexes/%s" % index_name, 'DELETE')

    # Queries the index. If no query parameter is set, retrieves all objects.
    def search(self, index_name, **args):
        return self.execute_request("/1/indexes/%s?%s" % (index_name, urllib.urlencode(args)))

    # Get one object in the index.
    def get(self, index_name, object_id, attributes=None):
        if attributes is not None:
            attributes = "?attributes=" + urllib.quote_plus(attributes)
        else:
            attributes = ""
        return self.execute_request("/1/indexes/%s/%s%s" % (index_name, object_id, attributes))

    # Add or replace an object (if the object does not exist, it will be created)
    def add(self, index_name, object_id, obj):
        if index_name in self.requests:
            requests = self.requests[index_name]
            requests.append({
                "method": 'PUT', 
                "path": "/1/indexes/%s/%s" % (index_name, object_id),
                "body": obj,
                })
            if len(requests) >= self.batch_size:
                self.end_batch(index_name)
                self.start_batch(index_name)
        else:
            obj = json.dumps(obj)
            return self.execute_request("/1/indexes/%s/%s" % (index_name, object_id), 'PUT', obj)

    # Updates part of an object (if the object does not exist, it will be created)
    def update(self, index_name, object_id, obj):
        if index_name in self.requests:
            requests = self.requests[index_name]
            requests.append({
                "method": 'POST', 
                "path": "/1/indexes/%s/%s/partial" % (index_name, object_id),
                "body": obj,
                })
            if len(requests) >= self.batch_size:
                self.end_batch(index_name)
                self.start_batch(index_name)
        else:
            obj = json.dumps(obj)
            return self.execute_request("/1/indexes/%s/%s/partial" % (index_name, object_id), 'POST', obj)

    # delete an existing object from an index
    def delete(self, index_name, object_id):
        return self.execute_request("/1/indexes/%s/%s" % (index_name, object_id), 'DELETE')

    # Changes index settings.
    def settings(self, index_name, **args):
        return self.execute_request("/1/indexes/%s/settings" % (index_name), 'PUT', json.dumps(args))
