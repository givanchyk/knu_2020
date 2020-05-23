
import unittest
from t30_1a import function


class TestFunction(unittest.TestCase): # Клас для тестів

    def test_1_equal(self):
        x = 0
        eps = 0.1
        value = function(x, eps)
        expected_value = round(1/(1 + x), 3)
        self.assertEqual(value, expected_value)

    def test_2_equal(self):
        x = 0.5
        eps = 1e-3
        value = round(function(x, eps), 3)
        expected_value = round(1/(1 + x), 3)
        self.assertEqual(value, expected_value)

    def test_3_equal(self):
        x = -0.1
        eps = 1e-10
        value = round(function(x, eps), 5)
        expected_value = round(1/(1 + x), 5)
        self.assertEqual(value, expected_value)

    def test_4_equal(self):
        x = -0.5
        eps = 1e-20
        value = round(function(x, eps), 15)
        expected_value = round(1/(1 + x), 3)
        self.assertEqual(value, expected_value)

    def test_5_true(self):
        x = 0.87
        eps = 1e-20
        value = round(function(x, eps), 16)
        expected_value = round(1/(1 + x), 16)
        self.assertTrue(abs(value - expected_value) < 1e-15)

    def test_6_true(self):
        x = 0.00023
        eps = 1e-20
        value = round(function(x, eps), 18)
        expected_value = round(1/(1 + x), 18)
        self.assertTrue(abs(value - expected_value) < 1e-15)

    def test_7_false(self):
        x = -0.123
        eps = 0.001
        value = function(x, eps)
        expected_value = round(1/(1 + x), 3)
        self.assertFalse(abs(value - expected_value) < 1e-15)


if __name__ == '__main__':
    unittest.main(verbosity=2)
    

