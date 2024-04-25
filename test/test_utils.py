import os
import unittest
import pandas as pd
from src.utils import csv_utils


def get_full_file(path) -> str:
    script_dir = os.path.dirname(__file__)
    return str(os.path.join(script_dir, path))


class TestUtils(unittest.TestCase):
    def test_get_results_from_data(self):
        data = pd.read_csv(get_full_file(path='files/characters.csv'))
        self.assertTrue((data.columns == ['Type', 'Name', 'Birthday', 'Kind', 'Colour']).all)
        self.assertTrue((data["Colour"].value_counts(normalize=True) * 100).round(2)["Orange"] == 66.67)

    def test_convert_date_field_to_date(self):
        data = pd.read_csv(get_full_file(path='files/worklog-details-report202404250906.csv'))
        self.assertTrue((data.columns == ["Assignee", "Worklog Description", "User", "Start Time", "Time Spent"]).all)
        csv_utils.customize_date_column_format(data, "Start Time", "%d/%m/%Y %H:%M %p", "%d/%m/%Y")
        self.assertEqual(data["Start Time"][197], '06/03/2024')

    def test_total_sum_by_id(self):
        data = pd.read_csv(get_full_file(path='files/worklog-details-report202404250906.csv'))
        self.assertTrue(
            (data.columns == ["Assignee", "Worklog Description", "User", "Start Time", "Time Spent (s)"]).all)
        self.assertEqual(csv_utils.get_total_sum_by_id(data, "Assignee", "Time Spent (s)").loc[3]["Time Spent (s)"],
                         50400)


if __name__ == '__main__':
    unittest.main()
