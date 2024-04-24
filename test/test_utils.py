import os
import unittest
import pandas as pd


class TestUtils(unittest.TestCase):
    def test_get_results_from_data(self):
        script_dir = os.path.dirname(__file__)
        full_path = os.path.join(script_dir, 'files/characters.csv')
        data = pd.read_csv(full_path)
        self.assertTrue((data.columns == ['Type', 'Name', 'Birthday', 'Kind', 'Colour']).all)
        self.assertTrue((data["Colour"].value_counts(normalize=True) * 100).round(2)["Orange"] == 66.67)


if __name__ == '__main__':
    unittest.main()
