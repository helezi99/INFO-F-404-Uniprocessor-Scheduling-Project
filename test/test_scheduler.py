import unittest
from scheduler.partitioned import partitioned_edf
from scheduler.global_ import global_edf
from scheduler.edf_k import edf_k

class TestScheduler(unittest.TestCase):
    def test_partitioned(self):
        tasks = [{'O': 0, 'C': 2, 'D': 5, 'T': 10}]
        result = partitioned_edf(tasks, 1, "ff", "iu")
        self.assertTrue(result)

    def test_global(self):
        tasks = [{'O': 0, 'C': 2, 'D': 5, 'T': 10}]
        result = global_edf(tasks, 1)
        self.assertTrue(result)

    def test_edf_k(self):
        tasks = [{'O': 0, 'C': 1, 'D': 3, 'T': 5}]
        result = edf_k(tasks, 1, k=1)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
