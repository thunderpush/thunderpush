import unittest


def suite():
    from thunderpush.testsuite import messenger

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(messenger.MessengerTestCase))
    return suite
