from thunderpush.messenger import Messenger
import unittest

class DummyThunderSocketHandler(object):
    dummyid = 1

    def __init__(self, *args, **kwargs):
        self.userid = "dummy_%d" % DummyThunderSocketHandler.dummyid
        self.connected = True

        DummyThunderSocketHandler.dummyid += 1

    def send(self, message):
        pass

    def broadcast(self, users, message):
        pass

class MessengerTestCase(unittest.TestCase):
    def setUp(self):
        self.messenger = Messenger('apikey', 'apisecret')

    def tearDown(self):
        self.messenger = None

    def test_is_online(self):
        user1 = DummyThunderSocketHandler()

        self.assertFalse(self.messenger.is_user_online(user1.userid))

        self.messenger.register_user(user1)
        self.assertTrue(self.messenger.is_user_online(user1.userid))

        self.messenger.unregister_user(user1)
        self.assertFalse(self.messenger.is_user_online(user1.userid))

    def test_user_counter(self):
        user1 = DummyThunderSocketHandler()
        user2 = DummyThunderSocketHandler()

        self.messenger.register_user(user1)
        self.messenger.register_user(user2)
        self.assertEqual(self.messenger.get_user_count(), 2)

        self.messenger.unregister_user(user1)
        self.assertEqual(self.messenger.get_user_count(), 1)

        self.messenger.unregister_user(user2)        
        self.assertEqual(self.messenger.get_user_count(), 0)

    def test_multiple_connections(self):
        # testing multiple connections from same userid
        user1 = DummyThunderSocketHandler()
        user2 = DummyThunderSocketHandler()
        userid = user2.userid = user1.userid

        self.messenger.register_user(user1)
        self.messenger.register_user(user2)

        self.assertEqual(self.messenger.get_user_count(), 2)
        self.assertTrue(userid in self.messenger.users)
        self.assertEqual(len(self.messenger.users[userid]), 2)
        self.assertTrue(user1 in self.messenger.users[userid])
        self.assertTrue(user2 in self.messenger.users[userid])

        self.messenger.unregister_user(user1)

        self.assertEqual(self.messenger.get_user_count(), 1)
        self.assertTrue(userid in self.messenger.users)
        self.assertEqual(len(self.messenger.users[userid]), 1)
        self.assertTrue(user2 in self.messenger.users[userid])

    def test_subscribe(self):
        user1 = DummyThunderSocketHandler()

        self.messenger.register_user(user1)
        self.messenger.subsribe_user_to_channel(user1, "test1")

        self.assertEqual(self.messenger.get_channel_user_count("test1"), 1)
        self.assertTrue(user1 in self.messenger.get_users_in_channel("test1"))

        self.messenger.unregister_user(user1)
        self.assertEqual(self.messenger.get_channel_user_count("test1"), 0)
        self.assertFalse(user1 in self.messenger.get_users_in_channel("test1"))

    def test_multiple_subscribe(self):
        # testing multiple subscribtions from same userid
        user1 = DummyThunderSocketHandler()
        user2 = DummyThunderSocketHandler()
        userid = user2.userid = user1.userid

        self.messenger.register_user(user1)
        self.messenger.register_user(user2)

        self.messenger.subsribe_user_to_channel(user1, "test1")
        self.messenger.subsribe_user_to_channel(user2, "test1")

        self.assertEqual(self.messenger.get_channel_user_count("test1"), 2)
        self.assertTrue(user1 in self.messenger.get_users_in_channel("test1"))
        self.assertTrue(user2 in self.messenger.get_users_in_channel("test1"))

        self.messenger.unregister_user(user1)

        self.assertEqual(self.messenger.get_channel_user_count("test1"), 1)
        self.assertFalse(user1 in self.messenger.get_users_in_channel("test1"))
        self.assertTrue(user2 in self.messenger.get_users_in_channel("test1"))

    def test_send_to_channel(self):        
        count = self.messenger.send_to_channel("test1", "test message")
        self.assertEqual(count, 0)

        user1 = DummyThunderSocketHandler()

        self.messenger.register_user(user1)
        self.messenger.subsribe_user_to_channel(user1, "test1")

        count = self.messenger.send_to_channel("test1", "test message")
        self.assertEqual(count, 1)

    def test_send_to_user(self): 
        user1 = DummyThunderSocketHandler()

        self.messenger.register_user(user1)
        count = self.messenger.send_to_user(user1.userid, "test message")

        self.assertEqual(count, 1)

    def test_send_to_multiple_users(self):
        user1 = DummyThunderSocketHandler()
        user2 = DummyThunderSocketHandler()
        userid = user2.userid = user1.userid

        self.messenger.register_user(user1)
        count = self.messenger.send_to_user(userid, "test message")

        self.assertEqual(count, 1)

        self.messenger.register_user(user2)
        count = self.messenger.send_to_user(userid, "test message")

        self.assertEqual(count, 2)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MessengerTestCase))
    return suite