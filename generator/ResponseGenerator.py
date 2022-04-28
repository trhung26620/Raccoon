from models.Response import Response

class ResponseGenerator:
    @staticmethod
    def generateResponseObject(responseData):
        if responseData:
            # if responseData.status_code:
            status = responseData.status_code
            # if responseData.headers:
            header = responseData.headers
            # if responseData.text:
            body = responseData.text
            # if responseData.elapsed.total_seconds():
            time = responseData.elapsed.total_seconds()
            response = Response(status, header, body, time)
            return response
        else:
            return None