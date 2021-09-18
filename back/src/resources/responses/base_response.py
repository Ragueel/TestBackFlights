import json

class BaseResponse(object):

    def __init__(self, status, data) -> None:
        self.status = status
        self.data = data

    def to_json(self)->str:
        return json.dumps({
            'status': self.status,
            'data': self.data
        })
