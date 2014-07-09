import cPickle
import base64
    

class PickleSerializer:
    
    def loads(self, s):
        try:
            return base64.b64decode(self.pickle.loads(s.encode('utf-8')))
        except EOFError:
            return ()

    def dumps(self, val):
        return base64.b64encode(self.pickle.dumps(val))


class JsonSerializer:
    def __init__(self):
        import json
        from bson import json_util
        self.json = json
        self.json_util = json_util

    def loads(self, s):
        return self.json.loads(s or '[]', object_hook=self.json_util.object_hook)

    def dumps(self, val):
        return self.json.dumps(val, default=self.json_util.default)
