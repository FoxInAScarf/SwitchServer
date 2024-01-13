from http.server import *

class ZHTTPRequestHandler(BaseHTTPRequestHandler):

    def sendFile(self, path, code):

        '''if not self.isFileFound(path):

            self.sendResponseCode(404)
            return'''

        if ".png" in path or ".jpg" in path or ".jpeg" in path:

            file = open(path, 'rb')
            self.sendRaw(file.read(), code)
            file.close()
            return

        file = open(path)
        self.sendText(file.read(), code)
        file.close()

    def sendText(self, text, code):

        self.sendRaw(bytes(text, "utf-8"), code)

    def sendRaw(self, data, code):

        self.sendResponseCode(code)
        self.wfile.write(data)

    def sendResponseCode(self, code):

        self.send_response(code)
        self.end_headers()

    def isFileFound(self, path):

        try:

            file = open(path)
            file.close()
            return True
        
        except:
            return False


    def getPostBody(self):

        bodyLength = int(self.headers["Content-Length"])
        return self.rfile.read(bodyLength).decode("utf-8")