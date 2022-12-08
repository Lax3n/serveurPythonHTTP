# Python 3 server example
from cgi import FieldStorage
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from typing import Any, Callable


theGetFunction: Any = None
thePostFunction: Any = None


@dataclass
class PostedData:
    name: str
    value: str

class MyRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global theHandler
        global theGetFunction
        theHandler = self
        theGetFunction(self.path)

    def sendFileChunk(self, chunk: str) -> None:
        self.wfile.write(bytes(chunk, "utf-8"))

    def sendBinaryFileChunk(self, chunk: bytes) -> None:
        self.wfile.write(chunk)



    def do_POST(self):
        '''handle post request paring and formatting before to delegate to students's post handler function'''
        global theHandler
        theHandler = self

        form: FieldStorage = FieldStorage(
                 fp=self.rfile,
                 headers=self.headers,
                 environ={"REQUEST_METHOD": "POST",
                          "CONTENT_TYPE": self.headers['Content-Type']})

        postedData: list[PostedData] = list([])
        allFieldStorages: list[FieldStorage] = form.value  # type: ignore
        i: int = int(0)
        for fs in allFieldStorages:
            # WARNING: crappy hack here to avoid extending PostedData with a filename. Good enough for the courses
            if (fs.filename != None):
                postedData.append(PostedData(fs.name+"Name", fs.filename))# type: ignore    
            postedData.append(PostedData(fs.name, fs.value))# type: ignore
            i += 1
                        
        global thePostFunction
        thePostFunction(postedData)


theHandler: MyRequestHandler

def sendResponse(code: int) -> None:
    '''This function send the response code to the client'''
    global theHandler
    theHandler.send_response(code)
    
def sendHeader(headerKeyword: str, headerValue: str) -> None:
    '''This function send a header keyword from the header, together with its value to the client
    WARNING: it closes the header directly after sending so a single couple can be sent in the header. 
    It is supposed to be used to send the ContentType of the content to be sent'''
    global theHandler
    theHandler.send_header(headerKeyword, headerValue)
    theHandler.end_headers()

def sendBinaryFileContent(content: bytes) -> None:
    '''This function send the content of a binary file to the client.'''
    global theHandler
    theHandler.sendBinaryFileChunk(content)
        
def sendTextualFileContent(content: str) -> None:
    '''This function send the textual content of a file encoded in utf-8 to the client.'''
    global theHandler
    theHandler.sendFileChunk(str(content))

def doesFileExist(path: str) -> bool:
    ''' This function returns True if the given path points to a valid file, False otherwise'''
    global theHandler
    return os.path.exists(path)

def setHandleGetRequest(f: Callable[[str], None])-> None:
    '''This function is used to define the actual get handler function for specific server request handling '''
    global theGetFunction
    theGetFunction = f

def setHandlePostRequest(f: Callable[[list[PostedData]], None])-> None:
    '''This function is used to define the actual post handler function for specific handling.
    The post handler function should take as parameter a list of PostedData,
    where PostedData is a strctured type with a name and a value, both of string type.'''
    global thePostFunction
    thePostFunction = f

def launchServer(hostName: str, serverPort: int) -> None:
    '''This function launch the python web server with the hostName IP, at the serverPort port
    This function does not return until the server dies. 
    WARNING: It should be used AFTER calling the setHandleGetRequest function'''
    webServer = HTTPServer((hostName, serverPort), MyRequestHandler)
    print("Server started http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    
    webServer.server_close()
    print("Server stopped.")


