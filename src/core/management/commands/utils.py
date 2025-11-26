from core import models
from django.utils import timezone
from django.conf import settings
import pandas as pd
from pathlib import Path


def cancel_all_plans(client_id, subscription_status_id):
    data = models.Subscription.objects.filter(
        client_id=client_id,
        cancellation_date__isnull=True
    )
    for item in data:
        item.cancellation_date = timezone.now()
        item.subscription_status_id = subscription_status_id
        item.save()
    print(f"{len(data)} planos cancelados")


def read_csv_file(csv_path):
    return pd.read_csv(
        csv_path,
        encoding="iso-8859-1"
    ).to_dict(orient="records")


def get_docs_file_path(path):
    base_path = settings.BASE_DIR.parent / "docs/"
    return Path(f"{base_path}/{path}")


def chose_file(path):
    base_path = settings.BASE_DIR.parent / "docs/"
    folder = Path(f"{base_path}/{path}")
    latest_file = max(folder.iterdir(), key=lambda f: f.stat().st_ctime)
    return str(latest_file)


def get_file_name(path):
    if not path:
        return path
    data = path.split("/")
    return data[len(data)-1]

