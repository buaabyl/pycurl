#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
# vi:ts=4:et

import pycurl
import sys
import unittest

class ErrorTest(unittest.TestCase):
    def setUp(self):
        self.curl = pycurl.Curl()

    def tearDown(self):
        self.curl.close()

    # error originating in libcurl
    def test_pycurl_error_libcurl(self):
        try:
            # perform without a url
            self.curl.perform()
        except pycurl.error:
            exc_type, exc = sys.exc_info()[:2]
            assert exc_type == pycurl.error
            # pycurl.error's arguments are libcurl errno and message
            self.assertEqual(2, len(exc.args))
            self.assertEqual(int, type(exc.args[0]))
            self.assertEqual(str, type(exc.args[1]))
            # unpack
            err, msg = exc
            self.assertEqual(pycurl.E_URL_MALFORMAT, err)
            # possibly fragile
            self.assertEqual('No URL set!', msg)

    # pycurl raises standard library exceptions in some cases
    def test_pycurl_error_stdlib(self):
        try:
            # set an option of the wrong type
            self.curl.setopt(pycurl.WRITEFUNCTION, True)
        except TypeError:
            exc_type, exc = sys.exc_info()[:2]

    # error originating in pycurl
    def test_pycurl_error_pycurl(self):
        try:
            # invalid option combination
            self.curl.setopt(pycurl.WRITEFUNCTION, lambda x: x)
            with open(__file__) as f:
                self.curl.setopt(pycurl.WRITEHEADER, f)
        except pycurl.error:
            exc_type, exc = sys.exc_info()[:2]
            assert exc_type == pycurl.error
            # for non-libcurl errors, arguments are just the error string
            self.assertEqual(1, len(exc.args))
            self.assertEqual(str, type(exc.args[0]))
            self.assertEqual('cannot combine WRITEHEADER with WRITEFUNCTION.', exc.args[0])
