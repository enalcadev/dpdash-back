import boto3
import pandas as pd
from src.utils.csv_utils import identify_results_by_frequency

sns = boto3.client('sns')
s3 = boto3.resource('s3')


def lambda_handler(event, context, csv, column, pct):
    data = pd.read_csv(csv)
    return identify_results_by_frequency(data, column, pct)
    #return {
    #    identify_results_by_frequency(data, column, pct),
    #    data
    #}
