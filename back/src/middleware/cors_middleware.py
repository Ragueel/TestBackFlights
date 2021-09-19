
class Crossdomain(object):
    async def process_response(self, req, resp, resource, req_succeeded):
        resp.set_header('Access-Control-Allow-Origin', '*')  # Change in prod
        resp.set_header('Access-Control-Allow-Methods',
                        'GET, PUT, POST, DELETE')
        resp.set_header('Access-Control-Allow-Credentials', 'true')
        resp.set_header(
            'Access-Control-Allow-Headers',
            'Origin, Authorization, Content-Type, X-Requested-With')