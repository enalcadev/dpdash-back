import pandas as pd


def csv_to_usable_data(file):
    return pd.read_csv(file)


def read_csv_rows(file_rows):
    for row in file_rows:
        print('\n'.join(row))
