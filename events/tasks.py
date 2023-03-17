import os
import uuid

import pandas as pd
import requests
from celery import shared_task

from events.models import Event


@shared_task
def export_events(webhook_url):
    events = Event.objects.all()
    df = pd.DataFrame.from_records(events.values())
    path = os.path.join(os.getcwd(), "events", "data", uuid.uuid4().hex + ".csv")
    df.to_csv(path)
    requests.post(webhook_url, data={"file_location": path})
