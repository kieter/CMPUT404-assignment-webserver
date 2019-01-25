#!/usr/bin/env python
# Copyright 2013 Abram Hindle
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
# run python freetests.py

from urllib import request
import unittest

BASEURL = "http://127.0.0.1:8080"

class TestYourWebserver(unittest.TestCase):
    def setUp(self,baseurl=BASEURL):
        """do nothing"""
        self.baseurl = baseurl

    def test_css(self):
        print("TEST_CSS")
        print("-"*20)

        url = self.baseurl + "/base.css"
        print("URL", url)
        req = request.urlopen(url, None, 3)
        self.assertTrue( req.getcode()  == 200 , "200 OK Not FOUND!")
        self.assertTrue( req.info().get_content_type() == "text/css", ("Bad mimetype for css! %s" % req.info().get_content_type()))

        print()

    def test_get_root(self):
        print("TEST_GET_ROOT")
        print("-"*20)

        url = self.baseurl + "/"
        print("URL", url)
        req = request.urlopen(url, None, 3)
        print("REQ", req)
        self.assertTrue( req.getcode()  == 200 , "200 OK Not FOUND!")

        print()

    def test_get_indexhtml(self):
        print("TEST_GET_INDEXHTML")
        print("-"*20)

        url = self.baseurl + "/index.html"
        req = request.urlopen(url, None, 3)
        self.assertTrue( req.getcode()  == 200 , "200 OK Not FOUND!")

        print()


    def test_get_404(self):
        print("TEST_GET_404")
        print("-"*20)

        url = self.baseurl + "/do-not-implement-this-page-it-is-not-found"
        try:
            req = request.urlopen(url, None, 3)
            self.assertTrue( False, "Should have thrown an HTTP Error!")
        except request.HTTPError as e:
            self.assertTrue( e.getcode()  == 404 , ("404 Not FOUND! %d" % e.getcode()))
        else:
            self.assertTrue( False, "Another Error was thrown!")
        
        print()


if __name__ == '__main__':
    unittest.main()
