import unittest


class LoaderTestCase(unittest.TestCase):
    def test_is_local_path(self):
        from qlient.schema.loader import is_local_path
        assert is_local_path(".")

        assert not is_local_path("http://test.test/graphql")
        assert not is_local_path("https://test.test/graphql")
        assert not is_local_path("file://test/test.json")


if __name__ == '__main__':
    unittest.main()
