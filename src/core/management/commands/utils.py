import re
import math
import unicodedata
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


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()


def set_case(ref):
    txt = normalize(ref)
    if "cancelamento por inadimplencia" in txt:
        return "canceled_by_non_payment"

    if "solicitado pela cliente" in txt:
        return "canceled_by_client"
    return None


def is_nan(data):
    try:
        if not data:
            return True
        if isinstance(data, float):
            if math.isnan(data):
                return True
        return False
    except Exception:
        return True


def is_real_email(email):
    try:
        if not email:
            return False
        if isinstance(email, float):
            if math.isnan(email):
                return False
        return True
    except Exception:
        return False


def get_client_by_email(email):
    data = models.Client.objects.filter(
        email=email
    ).first()
