#  coding: utf-8 
import socketserver
import os
import mimetypes
from http import HTTPStatus

DIR_PATH = os.getcwd() + "/"
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# Copyright 2019 Kieter Philip Lopez Balisnomo
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class MyWebServer(socketserver.BaseRequestHandler):
    def getFileContents(self, filePath): 
        file = open(filePath, "r")
        fileContents = file.read()
        file.close()
        return fileContents
    
    def getServerPath(self, requestPath):
        return DIR_PATH + "www" + requestPath
    
    def respond400(self, protocol, host, path):
        message400 = protocol + " " + str(HTTPStatus.NOT_FOUND.value) + " " + HTTPStatus.NOT_FOUND.phrase
        httpResponse400 = (message400 + "\r\n\r\n").encode()

        self.request.sendall(httpResponse400)
    
    def respond200(self, protocol, host, path):
        resolvedPath = path + "index.html" if path[-1] == "/" else path

        message200 = protocol + " " + str(HTTPStatus.OK.value) + " " + HTTPStatus.OK.phrase
        locationHeader = "Location: " + host + path

        maybeMimeType = mimetypes.guess_type(self.getServerPath(resolvedPath))[0]
        contentTypeHeader = "Content-Type: " + maybeMimeType

        responseBody = self.getFileContents(self.getServerPath(resolvedPath)) + "\r\n\r\n"

        httpResponse200 = "\r\n".join([message200, locationHeader, contentTypeHeader, responseBody]).encode()
        self.request.sendall(httpResponse200)
    
    def respond301(self, protocol, host, path):
        path += "/"
        if not os.path.exists(self.getServerPath(path) + "index.html"):
            self.respond400(protocol, host, path)
    
        message301 = protocol + " " + str(HTTPStatus.MOVED_PERMANENTLY.value) + " " + HTTPStatus.MOVED_PERMANENTLY.phrase
        locationHeader = "Location: " + host + path

        httpResponse301 = "\r\n".join([message301, locationHeader])
        httpResponse301 += "\r\n\r\n"
        httpResponse301 = httpResponse301.encode()

        self.request.sendall(httpResponse301)

    def respond405(self, protocol, host, path):
        message405 = protocol + " " + str(HTTPStatus.METHOD_NOT_ALLOWED.value) + " " + HTTPStatus.METHOD_NOT_ALLOWED.phrase

        httpResponse405 = (message405 + "\r\n\r\n").encode()
        self.request.sendall(httpResponse405)


    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.parseRequest(self.data)
    
    def isPathAllowed(self, requestPath):
        realPath = os.path.realpath(DIR_PATH + requestPath)
        isInDirectory = False if os.path.commonprefix([DIR_PATH, realPath]) == "/" else True
        return isInDirectory
    
    def doesPathExist(self, requestPath):
        serverPath = self.getServerPath(requestPath)
        return os.path.exists(serverPath) 
    
    def isFile(self, requestPath):
        serverPath = self.getServerPath(requestPath)
        return os.path.isfile(serverPath)
    
    def endsInSlash(self, requestPath):
        return requestPath[-1] == "/"

    def parseRequest(self, request):
        requestFullList = request.decode().split("\r\n")

        requestTypePathProto = requestFullList[0].split()
        requestHost = requestFullList[2].split()

        requestType = requestTypePathProto[0]
        requestPath = requestTypePathProto[1]
        requestProto = requestTypePathProto[2]

        if requestType != "GET":
            self.respond405()

        requestHost = requestHost[1]

        doesExist = self.doesPathExist(requestPath)
        isPathAllowed = self.isPathAllowed(requestPath)
        isFile = self.isFile(requestPath)
        endsInSlash = self.endsInSlash(requestPath)

        if doesExist and isPathAllowed and isFile:
            self.respond200(requestProto, requestHost, requestPath)
        elif doesExist and isPathAllowed and not isFile:
            if endsInSlash:
                self.respond200(requestProto, requestHost, requestPath)
            else:
                self.respond301(requestProto, requestHost, requestPath)
        else:
            self.respond400(requestProto, requestHost, requestPath)
        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
