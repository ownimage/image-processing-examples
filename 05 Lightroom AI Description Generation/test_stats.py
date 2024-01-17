import unittest

from stats import Stats


class TestStats(unittest.TestCase):
    stats = Stats()

    def setUp(self):
        self.stats = Stats()

    def tearDown(self):
        pass

    def test_add_first(self):
        # GIVEN
        expected = {1: {'count': 1, 'time': 0, 'time2': 0, 'first_time': 2.2, 'words': 4, 'words2': 16}}
        # WHEN
        self.stats.add(1, 2.2, 4)
        actual = self.stats.get()
        # THEN
        assert actual == expected

    def test_add_second(self):
        # GIVEN
        expected = {1: {'count': 2, 'time': 4, 'time2': 16, 'first_time': 2, 'words': 8, 'words2': 34}}
        # WHEN
        self.stats.add(1, 2, 3)
        self.stats.add(1, 4, 5)
        actual = self.stats.get()
        # THEN
        assert actual == expected

    def test_add_two_ids(self):
        # GIVEN
        expected = {
            1: {'count': 1, 'time': 0, 'time2': 0, 'first_time': 2, 'words': 3, 'words2': 9},
            2: {'count': 1, 'time': 0, 'time2': 0, 'first_time': 4, 'words': 5, 'words2': 25}
        }
        # WHEN
        self.stats.add(1, 2, 3)
        self.stats.add(2, 4, 5)
        actual = self.stats.get()
        # THEN
        assert actual == expected

    def test_get_cannot_be_modified(self):
        # GIVEN
        expected = {1: {'count': 1, 'time': 0, 'time2': 0, 'first_time': 2.2, 'words': 4, 'words2': 16}}
        self.stats.add(1, 2.2, 4)
        # WHEN
        modified = self.stats.get()
        modified[1]['count'] = 5
        actual = self.stats.get()
        # THEN
        assert actual == expected
        assert modified[1]['count'] == 5


if __name__ == "__main__":
    unittest.main()  # run all tests
