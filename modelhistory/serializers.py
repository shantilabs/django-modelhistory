import cPickle
import json


class PickleSerializer:
    def loads(self, s):
        try:
            return cPickle.loads(s.encode('utf-8'))
        except EOFError:
            return ()

    def dumps(self, val):
        return cPickle.dumps(val)


class JsonSerializer:
    def loads(self, s):
        return json.loads(s or '[]')

    def dumps(self, val):
        return json.dumps(val)
