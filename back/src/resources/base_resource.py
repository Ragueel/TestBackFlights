from src.resources.responses.base_response import BaseResponse
import falcon

class BaseResource(object):

    def make_success(self, resp: falcon.Response, result: BaseResponse) -> falcon.Response:
        resp.status=falcon.HTTP_200
        resp.text=result.to_json() 
        return resp