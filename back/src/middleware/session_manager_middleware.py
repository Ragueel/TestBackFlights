class SQLAlchemySessionManager:

    def __init__(self, Session):
        self.Session = Session

    async def process_resource(self, req, resp, resource, params):
        req.context.session = self.Session()
        pass

    async def process_response(self, req, resp, resource, req_succeeded):
        if hasattr(req.context, "session"):
            if not req_succeeded:
                req.context.session.rollback()
            req.context.session.close()