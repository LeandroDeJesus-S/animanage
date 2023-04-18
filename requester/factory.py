from .products import Requests, HttpX


class Requesters:
    @staticmethod
    def use_requests():
        req = Requests()
        return req
    
    @staticmethod
    def use_httpx():
        req = HttpX()
        return req
