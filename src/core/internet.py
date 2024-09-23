import http.client as httplib

class InternetUser:
    @staticmethod
    def internet_on():
        """
        See if the internet is on or not by sending a request to google.com.
        :return: A boolean
        """
        connection = httplib.HTTPConnection("google.com",timeout=3)
        try:
            # only header requested for fast operation
            connection.request("HEAD", "/")
            connection.close()  # connection closed
            return True
        except Exception:
            return False
