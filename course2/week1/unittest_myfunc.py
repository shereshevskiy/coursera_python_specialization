import unittest


# here may be any import
def my_func(x):
    return x**2


class TestSort(unittest.TestCase):
    def test_simple_cases(self):
        self.assertEqual(my_func(2), 4)
        self.assertEqual(my_func(4), 9)


if __name__ == "__main__":
    unittest.main()
