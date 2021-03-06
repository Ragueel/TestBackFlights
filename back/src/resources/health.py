from .base_resource import BaseResource
from .responses.base_response import BaseResponse
import falcon

class HealthResource(BaseResource):

    async def on_get(self, req,resp):
        return self.ok(resp, BaseResponse(falcon.HTTP_200, 'Healthy'))