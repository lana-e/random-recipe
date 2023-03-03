## INITIAL DEPLOYMENT CODE FROM GCLOUD TUTORIAL
import datetime

from flask import Flask, render_template

from google.cloud import datastore


## DATASTORE CODE FROM GCLOUD TUTORIAL
datastore_client = datastore.Client()

app = Flask(__name__)

def store_time(dt):
    entity = datastore.Entity(key=datastore_client.key('visit'))
    entity.update({
        'timestamp': dt
    })

    datastore_client.put(entity)


def fetch_times(limit):
    query = datastore_client.query(kind='visit')
    query.order = ['-timestamp']

    times = query.fetch(limit=limit)
    return times

@app.route('/')
def root():
    # Store the current access time in Datastore.
    store_time(datetime.datetime.now(tz=datetime.timezone.utc))

    # Fetch the most recent 10 access times from Datastore.
    times = fetch_times(10)
    # print(times)

    return render_template(
        'index.html', times=times)


## REPLACED WITH DATASTORE CODE ABOVE
# @app.route('/')
# def root():
#     # For the sake of example, use static information to inflate the template.
#     # This will be replaced with real information in later steps.
#     dummy_times = [datetime.datetime(2018, 1, 1, 10, 0, 0),
#                    datetime.datetime(2018, 1, 2, 10, 30, 0),
#                    datetime.datetime(2018, 1, 3, 11, 0, 0),
#                    ]

#     return render_template('index.html', times=dummy_times)


## CODE FROM INITIAL DEPLOYMENT
if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)

