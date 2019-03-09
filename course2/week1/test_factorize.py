import unittest


def factorize(x):
    """
    :param x: int, >=0
    :return: tuple, prime factors of x
    """
    pass


class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        """
        типы float и str (значения 'string', 1.5) вызывают исключение TypeError
        """
        cases = ("string", 1.5)
        for b in cases:
            with self.subTest(x=b):
                self.assertRaises(TypeError, factorize, b)

    def test_negative(self):
        """
        для отрицательных чисел -1, -10 и -100 вызывается исключение ValueError
        """
        cases = (-1, -10, -100)
        for b in cases:
            with self.subTest(x=b):
                self.assertRaises(ValueError, factorize, b)

    def test_zero_and_one_cases(self):
        """
        для числа 0 возвращается кортеж (0,), а для числа 1 кортеж (1,)
        """
        cases = ((0, (0,)), (1, (1,)))
        for b, a in cases:
            with self.subTest(x=b):
                self.assertEqual(a, factorize(b))

    def test_simple_numbers(self):
        """
        для простых чисел 3, 13, 29 возвращается кортеж, содержащий одно данное число
        """
        cases = (3, 13, 29)
        for b in cases:
            with self.subTest(x=b):
                self.assertEqual((b,), factorize(b))

    def test_two_simple_multipliers(self):
        """
        для чисел 6, 26, 121 возвращаются соответственно кортежи (2, 3), (2, 13) и (11, 11)
        """
        cases = ((6, (2, 3)), (26, (2, 13)), (121, (11, 11)))
        for b, a in cases:
            with self.subTest(x=b):
                self.assertEqual(a, factorize(b))

    def test_many_multipliers(self):
        """
         для чисел 1001 и 9699690 возвращаются соответственно кортежи (7, 11, 13) и (2, 3, 5, 7, 11, 13, 17, 19)
        """
        cases = ((1001, (7, 11, 13)), (9699690, (2, 3, 5, 7, 11, 13, 17, 19)))
        for b, a in cases:
            with self.subTest(x=b):
                self.assertEqual(a, factorize(b))


if __name__ == '__main__':
    unittest.main()
