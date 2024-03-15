import json
import os
import base64
import hashlib

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Metric, RunReportRequest

PORTAL_ID = os.environ['PORTAL_ID']
FOUNDATIONS_ID = os.environ['FOUNDATIONS_ID']
COOKBOOKS_ID = os.environ['COOKBOOKS_ID']

credentials_dict = {
  "type": "service_account",
  "project_id": "cisl-vast-pythia",
  "private_key_id": str(os.environ.get('PRIVATE_KEY_ID')),
  "private_key": str(os.environ.get('PRIVATE_KEY').replace('\\n', '\n')),
  "client_email": "pythia-metrics-api@cisl-vast-pythia.iam.gserviceaccount.com",
  "client_id": "113402578114110723940",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/pythia-metrics-api%40cisl-vast-pythia.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
client = BetaAnalyticsDataClient.from_service_account_info(credentials_dict)


def _run_total_users_report(property_id):
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


def get_metrics():
    metrics_dict = {}
    metrics_dict['Portal'] = _run_total_users_report(str(PORTAL_ID))
    metrics_dict['Foundations'] = _run_total_users_report(str(FOUNDATIONS_ID))
    metrics_dict['Cookbooks'] = _run_total_users_report(str(COOKBOOKS_ID))

    with open('user_metrics.json', 'w') as outfile:
        json.dump(metrics_dict, outfile)


if __name__ == '__main__':
    get_metrics()
