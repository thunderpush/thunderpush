import unittest


def suite():
    from thunderpush.tests import test_messenger, test_cli

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(test_messenger.MessengerTestCase))
    suite.addTest(unittest.makeSuite(test_cli.CLITestCase))

    return suite
