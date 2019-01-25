#  coding: utf-8 
import socketserver
import os
import mimetypes
from http import HTTPStatus

DIR_PATH = os.getcwd() + "/"
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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

    def respond200(self, protocol, host, path):
        # print("respond200\n")
        resolvedPath = path + "index.html" if path[-1] == "/" else path

        message200 = protocol + " " + str(HTTPStatus.OK.value) + " " + HTTPStatus.OK.phrase
        locationHeader = "Location: " + host + path

        maybeMimeType = mimetypes.guess_type(self.getServerPath(resolvedPath))[0]
        contentTypeHeader = "Content-Type: " + maybeMimeType
        # print("maybeMimeType", maybeMimeType)

        responseBody = self.getFileContents(self.getServerPath(resolvedPath)) + "\r\n\r\n"

        httpResponse200 = "\r\n".join([message200, locationHeader, contentTypeHeader, responseBody]).encode()
        # httpResponse200Encoded = httpResponse200.encode()
        print("-"*20)
        print("RESPONSE:\n")
        print(httpResponse200.decode())
        # print(self.request)
        self.request.sendall(httpResponse200)

        # print("RESPONSE?: ")
        # print(message200)
        # print(contentTypeHeader)
        # print(locationHeader)
        # print(responseBody)
        # print("resolvedPath: " + resolvedPath)
        # print("getServerPath:", self.getServerPath(resolvedPath))

    def respond400(self, protocol, host, path):
        message400 = protocol + " " + str(HTTPStatus.NOT_FOUND.value) + " " + HTTPStatus.NOT_FOUND.phrase

        print("-"*20)
        print("RESPONSE:\n")
        print(message400)

        httpResponse400 = (message400 + "\r\n").encode()
        self.request.sendall(httpResponse400)


    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("Got a request of: %s\n" % self.data)
        # print(self.request)
        # self.request.sendall(bytearray("OK",'utf-8'))
        # self.request.sendall(b"adfadfasdf")
        # print(bytearray("OK", "utf-8"))
        self.parseRequest(self.data)
    
    def isPathAllowed(self, requestPath):
        realPath = os.path.realpath(DIR_PATH + requestPath)
        print("realPath:", realPath)
        print("COMMONPATH: ", os.path.commonprefix([DIR_PATH, realPath]))
        isInDirectory = False if os.path.commonprefix([DIR_PATH, realPath]) == "/" else True
        print("isInDirectory:", isInDirectory)
        return isInDirectory
    
    def doesPathExist(self, requestPath):
        # print(requestPath)
        serverPath = self.getServerPath(requestPath)
        realPath = os.path.realpath(requestPath)

        # print("Path: " + self.getServerPath(requestPath))
        # print("dir_path:", DIR_PATH)
        # print("Path in common: " + os.path.commonprefix([DIR_PATH, realPath]))
        
        # print("requestPath exists?", os.path.exists(self.getServerPath(requestPath)))
        # print("requestPath:", requestPath)
        # print("realPath exists?", os.path.exists(self.getServerPath(realPath)))
        # print("realPath:", realPath)

        print("serverPath:", serverPath)
        return os.path.exists(serverPath) 

        # TODO: handle paths not ending in / and redirect

    def parseRequest(self, request):
        requestFullList = request.decode().split("\r\n")

        requestTypePathProto = requestFullList[0].split()
        requestHost = requestFullList[2].split()

        requestType = requestTypePathProto[0]
        requestPath = requestTypePathProto[1]
        # print("REQUEST PATH: " + requestPath)
        requestProto = requestTypePathProto[2]

        # TODO: Check if GET or not, otherwise 405
        # if requestType != "GET":
        #     respond405()
            

        requestHost = requestHost[1]

        # print("Type, Path, Proto, Host")
        # print(requestType, requestPath, requestProto, requestHost)
        doesExist = self.doesPathExist(requestPath)
        isPathAllowed = self.isPathAllowed(requestPath)
        print("doesExist: ", doesExist)
        print("isPathAllowed: ", isPathAllowed)
        # print(doesExist)

        if doesExist and isPathAllowed:
            self.respond200(requestProto, requestHost, requestPath)
        else:
            self.respond400(requestProto, requestHost, requestPath)
        




# def main():


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()


# HTTP/1.1 200 OK \r\n
# Header: afdasdf \r\n
# Header: afdasdf \r\n
# <body>
# </body>
# \r\n\r\n