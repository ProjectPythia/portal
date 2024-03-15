import json
import os

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Metric, RunReportRequest

PORTAL_ID = os.environ['portal_id']
FOUNDATIONS_ID = os.environ['foundations_id']
COOKBOOKS_ID = os.environ['cookbook_id']


def _run_total_users_report(property_id):

    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f'properties/{property_id}',
        dimensions=[],
        metrics=[Metric(name='activeUsers')],
        date_ranges=[DateRange(start_date='2020-03-31', end_date='today')],
    )

    response = client.run_report(request)

    total_users = 0
    for row in response.rows:
        total_users += int(row.metric_values[0].value)

    return total_users


def get_metrics(portal_id, foundations_id, cookbooks_id):
    metrics_dict = {}
    metrics_dict['Portal'] = _run_total_users_report(str(portal_id))
    metrics_dict['Foundations'] = _run_total_users_report(str(foundations_id))
    metrics_dict['Cookbooks'] = _run_total_users_report(str(cookbooks_id))

    with open('user_metrics.json', 'w') as outfile:
        json.dump(metrics_dict, outfile)


if __name__ == '__main__':
    get_metrics(PORTAL_ID, FOUNDATIONS_ID, COOKBOOKS_ID)
