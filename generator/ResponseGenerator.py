from models.Response import Response

class ResponseGenerator:
    @staticmethod
    def generateResponseObject(responseData):
        if responseData:
            status = responseData.status_code
            header = responseData.headers
            body = responseData.text
            time = responseData.elapsed.total_seconds()
            response = Response(status, header, body, time)
            return response
        else:
            return None