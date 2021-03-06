import requests
import schedule
from datetime import datetime
import time

from googleapiclient import discovery
from googleapiclient.http import MediaFileUpload
from oauth2client.client import GoogleCredentials


project_id = "bq-test-1062"
dataset_id = "twitch_data"
table_name = "arma3_example"
schema = [
  {"name": "check_time", "type": "TIMESTAMP", "mode": "nullable"},
  {"name": "streamer_name", "type": "STRING", "mode": "nullable"},
  {"name": "streamer_views", "type": "INTEGER", "mode": "nullable"}
]
data_path = "bq_test.csv"

clientId = {'client_id': '68tskg1eib5q4n0kzsa2i3wl0egcow', 'limit': '100', 'game' : 'Arma 3'}
twitch_request = requests.get('https://api.twitch.tv/kraken/streams/', params=clientId).json()

# [START make_post]
def load_data(schema_path, data_path, project_id, dataset_id, table_id):
    """Loads the given data file into BigQuery.
    Args:
        schema_path: the path to a file containing a valid bigquery schema.
            see https://cloud.google.com/bigquery/docs/reference/v2/tables
        data_path: the name of the file to insert into the table.
        project_id: The project id that the table exists under. This is also
            assumed to be the project id this request is to be made under.
        dataset_id: The dataset id of the destination table.
        table_id: The table id to load data into.
    """
    # Create a bigquery service object, using the application's default auth
    credentials = GoogleCredentials.get_application_default()
    bigquery = discovery.build('bigquery', 'v2', credentials=credentials)

    # Infer the data format from the name of the data file.
    source_format = 'CSV'
    if data_path[-5:].lower() == '.json':
        source_format = 'NEWLINE_DELIMITED_JSON'

    # Post to the jobs resource using the client's media upload interface. See:
    # http://developers.google.com/api-client-library/python/guide/media_upload
    insert_request = bigquery.jobs().insert(
        projectId=project_id,
        # Provide a configuration object. See:
        # https://cloud.google.com/bigquery/docs/reference/v2/jobs#resource
        body={
            'configuration': {
                'load': {
                    'schema': {
                        'fields': schema
                    },
                    'destinationTable': {
                        'projectId': project_id,
                        'datasetId': dataset_id,
                        'tableId': table_id
                    },
                    'sourceFormat': source_format,
                }
            }
        },
        media_body=MediaFileUpload(
            data_path,
            mimetype='application/octet-stream'))
    job = insert_request.execute()

    print('Waiting for job to finish...')

    status_request = bigquery.jobs().get(
        projectId=job['jobReference']['projectId'],
        jobId=job['jobReference']['jobId'])

    # Poll the job until it finishes.
    while True:
        result = status_request.execute(num_retries=2)

        if result['status']['state'] == 'DONE':
            if result['status'].get('errors'):
                raise RuntimeError('\n'.join(
                    e['message'] for e in result['status']['errors']))
            print('Job complete.')
            return

        time.sleep(1)
# [END make_post]


# [START main]

# [END main]

def get_date_from_twitch():
    print("start script")
    current_time = str(datetime.now())
    with open('bq_test.csv', 'w') as csv_file:
        for channel in twitch_request["streams"]:
            try:
                row = current_time + "," + channel["channel"]["name"] + "," + str(channel["viewers"]) + "\n"
                csv_file.write(row)
                print(row)
            except:
                row = current_time + "," + channel["channel"]["name"] + "," + str(0) + "\n"
                csv_file.write(row)
                print(row)
    print("start loading")
    load_data(
        schema,
        data_path,
        project_id,
        dataset_id,
        table_name)





schedule.every(30).minutes.do(get_date_from_twitch)
while True:
    schedule.run_pending()
    time.sleep(1)
# print(r.json())

# with open('file_tw.txt','w') as file:
#    json.dump(r, file)
