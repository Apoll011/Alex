import unittest

from core.list import Color, Item, ItemOrListDontExist, Lists

class ApplicationResources(unittest.TestCase):
    def setUp(self) -> None:
        self.list = Lists()

    def test_1_add_elements(self):
        i = Item("Tomato", quantity=3)
        self.list.add_to_list("shoping", i)
        
        self.assertListEqual(self.list.representation_of_all_elements("shoping"), ['3 Tomato'], "The lists dont match")

        i = Item("Tomato", quantity=4)
        self.list.add_to_list("shoping", i)
        self.assertListEqual(self.list.representation_of_all_elements("shoping"), ['7 Tomato'], "The lists dont match")

        i = Item("Tomato", quantity=4, color=Color.GREEN)
        self.list.add_to_list("shoping", i)
        self.assertListEqual(self.list.representation_of_all_elements("shoping"), ['7 Tomato', '4 Green Tomato'], "The lists dont match")

        with self.assertRaises(KeyError):
            self.list.representation_of_all_elements("shopping")

    def test_2_get(self):
        self.assertEqual(self.list.get("shoping"), "7 Tomato and 4 Green Tomato", "The text dont match")

        self.assertTrue(self.list.get("shoping", "tomato"), "Tomato set to false")
        self.assertFalse(self.list.get("shoping", "Onion"), "Onion set to false")
    
    def test_3_update(self):
        i = Item("Pencil", quantity=40, color=Color.BLUE)
        self.list.add_to_list("shoping", i)
        self.assertListEqual(self.list.representation_of_all_elements("shoping"), ['7 Tomato', '4 Green Tomato', '40 Blue Pencil'], "The lists dont match")
        
        i = Item("pen", quantity=4, color=Color.BLACK)
        self.list.update("shoping", "pencil", i)
        self.assertListEqual(self.list.representation_of_all_elements("shoping"), ['7 Tomato', '4 Green Tomato', '4 Black Pen'], "The lists dont match")

    def test_4_clear(self):
        self.list.clear("shoping", "pen")
        self.assertListEqual(self.list.representation_of_all_elements("shoping"), ['7 Tomato', '4 Green Tomato'], "The lists dont match")
        self.list.clear("shoping")

        self.assertEqual(self.list.get("shoping"), "Your shoping list is empy!")

        with self.assertRaises(ItemOrListDontExist):
            self.list.remove_item("shoping", "pen")

if __name__ == '__main__':
    unittest.main()
