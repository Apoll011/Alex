import http.client as httplib

class InternetUser:
    internet_is_on: bool

    def internet_on(self):
        connection = httplib.HTTPConnection("google.com",timeout=3)
        try:
            # only header requested for fast operation
            connection.request("HEAD", "/")
            connection.close()  # connection closed
            return True
        except Exception as exep:
            return False
