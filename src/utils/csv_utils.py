import pandas as pd


def csv_to_usable_data(file):
    return pd.read_csv(file)


def customize_date_column_format(data, column, initial_format, end_format):
    data[column] = pd.to_datetime(data[column], format=initial_format)
    data[column] = data[column].dt.strftime(end_format)


def read_csv_rows(file_rows):
    for row in file_rows:
        print('\n'.join(row))
