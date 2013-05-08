import json
import urllib
import urllib2

class Client:
    def __init__(self, host, app_id, api_key, batch_size=1000):
        self.host = host
        self.app_id = app_id
        self.api_key = api_key
        self.batch_size = batch_size
        self.requests = {}
        self.opener = urllib2.build_opener(urllib2.HTTPHandler)

    def set_headers(self, request, method):
        request.add_header('Content-Type', 'application/json; charset=utf-8')
        request.add_header('X-Algolia-API-Key', self.api_key)
        request.add_header('X-Algolia-Application-Id', self.app_id)
        request.get_method = lambda: method

    def execute_request(self, request, method='GET'):
        self.set_headers(request, method)
        try:
            return json.loads(self.opener.open(request).read())
        except urllib2.HTTPError, e:
            return json.loads(e.read())

    def start_batch(self, index_name):
        if index_name not in self.requests:
            self.requests[index_name] = []

    def end_batch(self, index_name):
        response = None
        if index_name in self.requests:
            requests = self.requests[index_name]
            if len(requests) > 0:
                data = json.dumps({'requests': requests})
                request = urllib2.Request("https://%s/1/indexes/%s/batch" % (self.host, index_name), data=data)
                response = self.execute_request(request, 'POST')
            del self.requests[index_name]
        return response

    # Lists your indexes. Returns also a pendingTask flag per index that indicates if it has remaining task(s) running.
    def get_index(self, index_name):
        request = urllib2.Request("https://%s/1/indexes/%s" % (self.host, index_name))
        return self.execute_request(request)

    # delete an existing index
    def delete_index(self, index_name):
        request = urllib2.Request("https://%s/1/indexes/%s" % (self.host, index_name))
        return self.execute_request(request, 'DELETE')

    # Queries the index. If no query parameter is set, retrieves all objects.
    def search(self, index_name, **args):
        request = urllib2.Request("https://%s/1/indexes/%s?%s" % (self.host, index_name, urllib.urlencode(args)))
        return self.execute_request(request)

    # Get one object in the index.
    def get(self, index_name, object_id, attributes=None):
        if attributes is not None:
            attributes = "?attributes=" + urllib.quote_plus(attributes)
        else:
            attributes = ""
        request = urllib2.Request("https://%s/1/indexes/%s/%s%s" % (self.host, index_name, object_id, attributes))
        return self.execute_request(request)

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
            request = urllib2.Request("https://%s/1/indexes/%s/%s" % (self.host, index_name, object_id), data=obj)
            return self.execute_request(request, 'PUT')

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
            request = urllib2.Request("https://%s/1/indexes/%s/%s/partial" % (self.host, index_name, object_id), data=obj)
            return self.execute_request(request, 'POST')

    # delete an existing object from an index
    def delete(self, index_name, object_id):
        request = urllib2.Request("https://%s/1/indexes/%s/%s" % (self.host, index_name, object_id))
        return self.execute_request(request, 'DELETE')

    # Changes index settings.
    def settings(self, index_name, **args):
        request = urllib2.Request("https://%s/1/indexes/%s/settings" % (self.host, index_name), json.dumps(args))
        return self.execute_request(request, 'PUT')
