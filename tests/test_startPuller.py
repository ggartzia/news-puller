import unittest

from news_puller.startPuller import hello


class HelloTestCase(unittest.TestCase):

    def test_hello(self):
        self.assertEqual(
            hello(),
            'Hello world!'
        )
