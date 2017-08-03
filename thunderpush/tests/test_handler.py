import mock
import unittest
from thunderpush.handler import ThunderSocketHandler


class HandlerTestCase(unittest.TestCase):
    @mock.patch('thunderpush.handler.ThunderSocketHandler.handle_connect')
    def test_command_parser(self, mock_handler):
        handler = ThunderSocketHandler(mock.Mock())
        handler.process_message('CONNECT 1:2')
        mock_handler.assert_called_once_with('1:2')
