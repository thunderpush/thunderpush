import unittest


def suite():
    from thunderpush.tests import test_messenger, test_cli, test_api

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(test_messenger.MessengerTestCase))
    suite.addTest(unittest.makeSuite(test_cli.CLITestCase))
    suite.addTest(unittest.makeSuite(test_api.APITestCase))

    return suite
