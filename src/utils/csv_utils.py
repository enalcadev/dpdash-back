import pandas as pd


def customize_date_column_format(data, column, initial_format, end_format):
    data[column] = pd.to_datetime(data[column], format=initial_format)
    data[column] = data[column].dt.strftime(end_format)


def get_total_sum_by_id(data, id_column, to_sum_column):
    return data.groupby(id_column).sum()[to_sum_column].reset_index()


def identify_low_frequency_results(data, column, pct):
    res = (data[column].value_counts(normalize=True) * 100).round(2)
    return res[res < pct].index
