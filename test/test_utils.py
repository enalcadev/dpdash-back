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

    def test_identify_low_frequency_results(self):
        data = pd.read_csv(get_full_file(path='files/worklog-details-report202404250906.csv'))
        self.assertTrue((csv_utils.identify_results_by_frequency(data, "Worklog Description", 1).unknown ==
                         ['Geoc actualizado', 'SGE listo', 'GOVER funcionando',
                          'Hores empleadas en la configuració de les VPN y GEOC',
                          'Configurar proyecto GOVR', 'GOVER', 'SAI', 'RITC',
                          'Ayudando a Geoffrey a configurar GEOC',
                          'Soporte a Jonathan con configuración SGE+', 'Hores empleadas en GEOC',
                          'SGE/GOVER', 'Horas empleadas en la confirguración de VPN Gene',
                          'Horas empleadas en GEOC', 'Configuración de GEOC', 'GOVR + SGE',
                          'He estado mirando que todos los proyectos funcionaran, y me puse también a instalar GEOC',
                          'ICT / GOVR', 'FORMATEO', 'ASISTENCIA TECNICA',
                          'GOVR. Muchos problemas con base de datos',
                          'Ayuda sge, se ha conseguido acabar de instalar',
                          'Se realizo la Miració de ICT', 'Migració de ICT',
                          'Problemas con la Migració de ICT',
                          'Una serie de problemas con la migracion en RITC solucionados',
                          'Migracion de RITC', 'GEOC - Working']).all())

    def test_replace_unwanted_results(self):
        replacements_dictionary = {
            'Configurar proyecto GOVR': 'GOVR',
            'Migracion de GOVR': 'GOVR',
            'GOVER funcionando': 'GOVR',
            'ICT / GOVR': 'GOVR',
            'SGE/GOVER': 'GOVR',
            'GOVER': 'GOVR',
            'Geoc': 'GEOC',
            'GEOC - Working': 'GEOC',
            'Geoc actualizado': 'GEOC',
            'Configuración de GEOC': 'GEOC',
            'Horas empleadas en GEOC': 'GEOC',
            'Hores empleadas en GEOC': 'GEOC',
            'Ayudando a Geoffrey a configurar GEOC': 'GEOC',
            'GOVR. Muchos problemas con base de datos': 'GEOC',
            'Hores empleadas en la configuració de les VPN y GEOC': 'GEOC',
            'He estado mirando que todos los proyectos funcionaran, y me puse también a instalar GEOC': 'GEOC',
            'ICT': 'ICT/RITC',
            'RITC': 'ICT/RITC',
            'Migració de ICT': 'ICT/RITC',
            'Migracion de RITC': 'ICT/RITC',
            'Se realizo la Miració de ICT': 'ICT/RITC',
            'Problemas con la Migració de ICT': 'ICT/RITC',
            'Una serie de problemas con la migracion en RITC solucionados': 'ICT/RITC',
            'Ayuda sge, se ha conseguido acabar de instalar': 'SGE',
            'Soporte a Jonathan con configuración SGE+': 'SGE',
            'Configuración de SGE': 'SGE',
            'GOVR + SGE': 'SGE',
            'SGE listo': 'SGE',
            'SGE+': 'SGE',
        }
        data = pd.read_csv(get_full_file(path='files/worklog-details-report202404250906.csv'))
        csv_utils.replace_unknown_values(data, "Worklog Description", replacements_dictionary)
        self.assertTrue((csv_utils.identify_results_by_frequency(data, "Worklog Description", 1).valid == ['SGE', 'GEOC',
                         'RACC', 'GOVR', 'ICT/RITC']).all())


if __name__ == '__main__':
    unittest.main()
