from django.test import TestCase


class AliveTest(TestCase):
    msg = ''

    def setUp(self):
        self.msg = 'alive'

    def test_echo_echo_test(self):
        self.assertEquals('alive', self.msg)
