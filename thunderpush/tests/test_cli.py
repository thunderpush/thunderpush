import unittest
from thunderpush.runner import parse_args


class CLITestCase(unittest.TestCase):
    def test_args(self):
        self.assertRaises(SystemExit, parse_args, [])
        self.assertRaises(SystemExit, parse_args, ['foo'])

        args = vars(parse_args(['-d', '-p 1234', '-H foobar', 'foo', 'bar']))
        self.assertEqual(args.get('clientkey', None), 'foo')
        self.assertEqual(args.get('apikey', None), 'bar')
        self.assertEqual(args.get('DEBUG', None), True)
        self.assertEqual(args.get('PORT', None), 1234)
        self.assertEqual(args.get('HOST', None).strip(), 'foobar')
