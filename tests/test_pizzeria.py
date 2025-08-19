import unittest
from restaurant.nutritional import Nutritional
from restaurant.pizzeria import Pizzeria
from restaurant.exceptions import TrayException


class TestR0(unittest.TestCase):
    def test_abstract(self):
        self.assertRaises(TypeError, Nutritional)


class TestR1(unittest.TestCase):
    def setUp(self):
        self._pz = Pizzeria()

    def test_get_ingredients(self):
        self._pz.create_ingredient("ing1", 5.2, 7.9, 11.4)
        self._pz.create_ingredient("ing2", 2.2345, 5, 19.3)
        self._pz.create_ingredient("ing3", 7, 9, 11)

        self.assertEqual("ing1", self._pz.get_ingredient("ing1").name)
        self.assertEqual("ing2", self._pz.get_ingredient("ing2").name)
        self.assertEqual("ing3", self._pz.get_ingredient("ing3").name)

    def test_nutritional_values(self):
        ing1 = self._pz.create_ingredient("ing1", 5.2, 7.9, 11.4)
        self.assertEqual(ing1.name, "ing1")
        self.assertAlmostEqual(5.2, ing1.carbs)
        self.assertAlmostEqual(7.9, ing1.fat)
        self.assertAlmostEqual(11.4, ing1.proteins)

    def test_ingredient_order(self):
        ing1 = self._pz.create_ingredient("abc", 1, 2, 3)
        ing2 = self._pz.create_ingredient("def", 4, 5, 6)
        ing3 = self._pz.create_ingredient("ghi", 7, 9, 11)
        ingredients = [ing2, ing3, ing1]
        ingredients.sort()
        self.assertEqual(["abc", "def", "ghi"], [ing.name for ing in ingredients])

    def test_str(self):
        ing2 = self._pz.create_ingredient("ing2", 2.2345, 5, 19.3)
        self.assertEqual("ing2 2.23 5.00 19.30", str(ing2))

    def test_get_ingredients_complex(self):
        self._pz.create_ingredient("ing2", 2.2345, 5, 19.3)
        self._pz.create_ingredient("ing3", 7, 9, 11)

        ing2 = self._pz.get_ingredient("ing2")
        ing3 = self._pz.get_ingredient("ing3")

        self.assertEqual("ing2", ing2.name)
        self.assertAlmostEqual(2.2345, ing2.carbs)
        self.assertAlmostEqual(5.0, ing2.fat)
        self.assertAlmostEqual(19.3, ing2.proteins)

        self.assertEqual("ing3", ing3.name)
        self.assertAlmostEqual(7.0, ing3.carbs)
        self.assertAlmostEqual(9.0, ing3.fat)
        self.assertAlmostEqual(11.0, ing3.proteins)


class TestR2(unittest.TestCase):
    def setUp(self):
        self._pz = Pizzeria()
        self._pz.create_ingredient("ing1", 5.2, 7.9, 11.4)
        self._pz.create_ingredient("ing2", 2.2345, 5, 19.3)
        self._pz.create_ingredient("ing3", 7, 9, 11)

    def test_tray_one(self):
        self._pz.create_pizza_tray("pizza1", 5)
        self._pz.add_tray_ingredient("pizza1", "ing2", (1, 2), 3, 27)
        tray = self._pz.get_pizza_tray("pizza1")
        self.assertEqual("pizza1", tray.name)
        self.assertAlmostEqual(2.2345 * 27 / 100, tray.carbs)
        self.assertAlmostEqual(5 * 27 / 100, tray.fat)
        self.assertAlmostEqual(19.3 * 27 / 100, tray.proteins)

    def test_tray_two(self):
        self._pz.create_pizza_tray("pizza1", 5)
        self._pz.add_tray_ingredient("pizza1", "ing2", (0, 3), 2, 15)
        self._pz.add_tray_ingredient("pizza1", "ing1", (3, 3), 2, 35)
        tray = self._pz.get_pizza_tray("pizza1")
        self.assertEqual("pizza1", tray.name)
        self.assertAlmostEqual(2.2345 * 15 / 100 + 5.2 * 35 / 100, tray.carbs)
        self.assertAlmostEqual(5 * 15 / 100 + 7.9 * 35 / 100, tray.fat)
        self.assertAlmostEqual(19.3 * 15 / 100 + 11.4 * 35 / 100, tray.proteins)

    def test_tray_overlap(self):
        self._pz.create_pizza_tray("pizza1", 5)
        self._pz.add_tray_ingredient("pizza1", "ing2", (0, 3), 2, 15)
        self._pz.add_tray_ingredient("pizza1", "ing1", (3, 3), 2, 35)
        self._pz.add_tray_ingredient("pizza1", "ing3", (1, 1), 3, 11)
        tray = self._pz.get_pizza_tray("pizza1")
        self.assertEqual("pizza1", tray.name)
        self.assertAlmostEqual((2.2345 * 15 + 5.2 * 35 + 7 * 11) / 100, tray.carbs)
        self.assertAlmostEqual((5 * 15 + 7.9 * 35 + 9 * 11) / 100, tray.fat)
        self.assertAlmostEqual((19.3 * 15 + 11.4 * 35 + 11 * 11) / 100, tray.proteins)

    def test_tray_exception(self):
        self._pz.create_pizza_tray("pizza1", 7)
        self._pz.create_pizza_tray("pizza2", 9)
        self._pz.create_pizza_tray("pizza3", 4)
        self._pz.add_tray_ingredient("pizza1", "ing2", (0, 3), 2, 15)
        self.assertRaises(TrayException, self._pz.add_tray_ingredient, "pizza2", "ing2", (-1, 0), 2, 15)
        self.assertRaises(TrayException, self._pz.add_tray_ingredient, "pizza3", "ing2", (1, 1), 5, 15)


class TestR3(unittest.TestCase):
    def setUp(self):
        self._pz = Pizzeria()
        self._pz.create_ingredient("ing1", 1, 2, 3)
        self._pz.create_ingredient("ing2", 4, 5, 6)
        self._pz.create_ingredient("ing3", 7, 8, 9)
        self._pz.create_pizza_tray("pizza", 4)

    def test_slice(self):
        self._pz.add_tray_ingredient("pizza", "ing3", (1, 1), 2, 15)
        self._pz.add_tray_ingredient("pizza", "ing1", (0, 0), 2, 15)
        self.assertEqual(["ing1"], [i.name for i in self._pz.get_slice("pizza", (0, 1))])
        self.assertEqual(["ing1"], [i.name for i in self._pz.get_slice("pizza", (1, 0))])
        self.assertEqual(["ing1"], [i.name for i in self._pz.get_slice("pizza", (1, 0))])
        self.assertEqual(["ing3", "ing1"], [i.name for i in self._pz.get_slice("pizza", (1, 1))])
        self.assertEqual(["ing3"], [i.name for i in self._pz.get_slice("pizza", (2, 1))])
        self.assertEqual(["ing3"], [i.name for i in self._pz.get_slice("pizza", (2, 2))])
        self.assertEqual(["ing3"], [i.name for i in self._pz.get_slice("pizza", (1, 2))])

    def test_slice_duplicate(self):
        self._pz.add_tray_ingredient("pizza", "ing3", (1, 1), 2, 15)
        self._pz.add_tray_ingredient("pizza", "ing2", (0, 0), 4, 15)
        self._pz.add_tray_ingredient("pizza", "ing3", (0, 0), 2, 15)
        self.assertEqual(["ing2", "ing3"], [i.name for i in self._pz.get_slice("pizza", (1, 0))])
        self.assertEqual(["ing3", "ing2", "ing3"], [i.name for i in self._pz.get_slice("pizza", (1, 1))])
        self.assertEqual(["ing3", "ing2"], [i.name for i in self._pz.get_slice("pizza", (2, 2))])

    def test_layer_full(self):
        self._pz.add_tray_ingredient("pizza", "ing1", (0, 0), 2, 15)
        self._pz.add_tray_ingredient("pizza", "ing2", (1, 2), 2, 15)
        self._pz.add_tray_ingredient("pizza", "ing3", (0, 0), 4, 15)
        expected = [
            ['ing1', 'ing1', 'ing3', 'ing3'],
            ['ing1', 'ing1', 'ing2', 'ing2'],
            ['ing3', 'ing3', 'ing2', 'ing2'],
            ['ing3', 'ing3', 'ing3', 'ing3']
        ]
        self.assertEqual(expected, self._pz.get_layer("pizza", 0))

    def test_layer(self):
        self._pz.add_tray_ingredient("pizza", "ing1", (0, 0), 2, 15)
        self._pz.add_tray_ingredient("pizza", "ing2", (1, 1), 2, 15)
        self._pz.add_tray_ingredient("pizza", "ing3", (0, 0), 4, 15)
        expected_1 = [
            ['ing3', 'ing3', None, None],
            ['ing3', 'ing2', 'ing3', None],
            [None, 'ing3', 'ing3', None],
            [None, None, None, None]
        ]
        expected_2 = [
            [None, None, None, None],
            [None, 'ing3', None, None],
            [None, None, None, None],
            [None, None, None, None]
        ]
        self.assertEqual(expected_1, self._pz.get_layer("pizza", 1))
        self.assertEqual(expected_2, self._pz.get_layer("pizza", 2))


class TestR4(unittest.TestCase):
    def setUp(self) -> None:
        self._pz = Pizzeria()
        self._pz.create_ingredient("ing1", 1, 2, 3)
        self._pz.create_ingredient("ing2", 4, 5, 6)
        self._pz.create_ingredient("ing3", 7, 8, 9)
        self._pz.create_pizza_tray("pizza", 5)

    def test_contiguous_with_empty(self):
        self._pz.add_tray_ingredient("pizza", "ing2", (0, 2), 3, 123)
        portion = self._pz.get_contiguous_portion("pizza", (1, 1), "ing2")
        expected = [
            [True, True, False, False, False],
            [True, True, False, False, False],
            [True, True, False, False, False],
            [True, True, True, True, True],
            [True, True, True, True, True]
        ]
        self.assertEqual(expected, portion)

    def test_contiguous_separated_multi(self):
        self._pz.add_tray_ingredient("pizza", "ing3", (0, 2), 3, 123)
        self._pz.add_tray_ingredient("pizza", "ing1", (0, 0), 5, 123)
        self._pz.add_tray_ingredient("pizza", "ing3", (3, 0), 2, 123)
        portion = self._pz.get_contiguous_portion("pizza", (3, 2), "ing3")
        expected = [
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, True, True, True],
            [False, False, True, True, True]
        ]
        self.assertEqual(expected, portion)

    def test_contiguous_separated_base(self):
        self._pz.add_tray_ingredient("pizza", "ing1", (0, 0), 5, 123)
        self._pz.add_tray_ingredient("pizza", "ing2", (0, 0), 2, 123)
        self._pz.add_tray_ingredient("pizza", "ing2", (2, 2), 2, 123)
        self._pz.add_tray_ingredient("pizza", "ing2", (3, 2), 2, 123)
        self._pz.add_tray_ingredient("pizza", "ing2", (1, 3), 2, 123)
        portion = self._pz.get_contiguous_portion("pizza", (1, 2), "ing2")
        expected = [
            [False, False, True, True, True],
            [False, False, True, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False]
        ]
        self.assertEqual(expected, portion)

    def test_contiguous_all_good(self):
        self._pz.add_tray_ingredient("pizza", "ing1", (0, 0), 5, 123)
        self._pz.add_tray_ingredient("pizza", "ing2", (0, 0), 2, 123)
        self._pz.add_tray_ingredient("pizza", "ing2", (2, 2), 2, 123)
        self._pz.add_tray_ingredient("pizza", "ing2", (3, 2), 2, 123)
        self._pz.add_tray_ingredient("pizza", "ing2", (1, 3), 2, 123)
        portion = self._pz.get_contiguous_portion("pizza", (1, 2), "ing3")
        expected = [
            [True, True, True, True, True],
            [True, True, True, True, True],
            [True, True, True, True, True],
            [True, True, True, True, True],
            [True, True, True, True, True]
        ]
        self.assertEqual(expected, portion)


class TestR5(unittest.TestCase):
    def setUp(self):
        self._pz = Pizzeria()
        self._pz.create_ingredient("ing1", 5, 4, 1)
        self._pz.create_ingredient("ing2", 45, 30, 100)
        self._pz.create_ingredient("ing3", 48, 11, 32)
        self._pz.create_ingredient("ing4", 10, 20, 30)
        self._pz.create_pizza_tray("pizza", 5)
        self._pz.add_tray_ingredient("pizza", "ing1", (0, 0), 5, 123)
        self._pz.add_tray_ingredient("pizza", "ing2", (0, 0), 5, 123)
        self._pz.add_tray_ingredient("pizza", "ing3", (0, 0), 5, 123)
        self._pz.add_tray_ingredient("pizza", "ing4", (0, 0), 5, 123)

    def test_lambda_1(self):
        ingredients = self._pz.sort_slice("pizza", (1, 1), lambda x: x.proteins + x.carbs - x.fat)
        self.assertEqual(['ing1', 'ing4', 'ing3', 'ing2'], [i.name for i in ingredients])

    def test_lambda_2(self):
        ingredients = self._pz.sort_slice("pizza", (1, 1), lambda x: 1/x.fat)
        self.assertEqual(['ing2', 'ing4', 'ing3', 'ing1'], [i.name for i in ingredients])
