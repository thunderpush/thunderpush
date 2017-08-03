import unittest


def suite():
    from thunderpush.tests import (
        test_api,
        test_cli,
        test_handler,
        test_messenger,
    )

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(test_api.APITestCase))
    suite.addTest(unittest.makeSuite(test_cli.CLITestCase))
    suite.addTest(unittest.makeSuite(test_handler.HandlerTestCase))
    suite.addTest(unittest.makeSuite(test_messenger.MessengerTestCase))

    return suite
